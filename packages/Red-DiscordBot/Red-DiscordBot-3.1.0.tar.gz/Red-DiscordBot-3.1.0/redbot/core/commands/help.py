# This is a full replacement of discord.py's help command
# Signatures are not guaranteed to be unchanging in this file.
# At a later date when this is more set in stone, this warning will be removed.
# At said later date, there should also be things added to support extra formatter
# registration from 3rd party cogs.
#
# This exists due to deficiencies in discord.py which conflict
# with our needs for per-context help settings
# see https://github.com/Rapptz/discord.py/issues/2123
#
# While the issue above discusses this as theoretical, merely interacting with config within
# the help command preparation was enough to cause
# demonstrable breakage in 150 help invokes in a 2 minute window.
# This is not an unreasonable volume on some already existing Red instances,
# especially since help is invoked for command groups
# automatically when subcommands are not provided correctly as user feedback.
#
# The implemented fix is in
# https://github.com/Rapptz/discord.py/commit/ad5beed8dd75c00bd87492cac17fe877033a3ea1
#
# While this fix would handle our immediate specific issues, it's less appropriate to use
# Where we do not have a downstream consumer to consider.
# Simply modifying the design to not be susceptible to the issue,
# rather than adding copy and deepcopy use in multiple places is better for us
#
# Additionally, this gives our users a bit more customization options including by
# 3rd party cogs down the road.

from collections import namedtuple
from typing import Union, List, AsyncIterator, Iterable, cast

import discord
from discord.ext import commands as dpy_commands

from . import commands
from .context import Context
from ..i18n import Translator
from ..utils import menus, fuzzy_command_search, format_fuzzy_results
from ..utils.chat_formatting import box, pagify

__all__ = ["red_help", "RedHelpFormatter"]

T_ = Translator("Help", __file__)

HelpTarget = Union[commands.Command, commands.Group, commands.Cog, dpy_commands.bot.BotBase, str]

# The below could be a protocol if we pulled in typing_extensions from mypy.
SupportsCanSee = Union[commands.Command, commands.Group, dpy_commands.bot.BotBase, commands.Cog]

EmbedField = namedtuple("EmbedField", "name value inline")
EMPTY_STRING = "\N{ZERO WIDTH SPACE}"


class NoCommand(Exception):
    pass


class NoSubCommand(Exception):
    def __init__(self, *, last, not_found):
        self.last = last
        self.not_found = not_found


class RedHelpFormatter:
    """
    Red's help implementation

    This is intended to be overridable in parts to only change some behavior.

    While currently, there is a global formatter, later plans include a context specific
    formatter selector as well as an API for cogs to register/un-register a formatter with the bot.

    When implementing your own formatter, at minimum you must provide an implementation of 
    `send_help` with identical signature.

    While this exists as a class for easy partial overriding, most implementations
    should not need or want a shared state.
    """

    # Class vars for things which should be configurable at a later date but aren't now
    # Technically, someone can just use a cog to switch these in real time for now.

    USE_MENU = False
    CONFIRM_UNAVAILABLE_COMMAND_EXISTENCES = False
    SHOW_HIDDEN = False
    VERIFY_CHECKS = True

    async def send_help(self, ctx: Context, help_for: HelpTarget = None):
        """ 
        This delegates to other functions. 
        
        For most cases, you should use this and only this directly.
        """
        if help_for is None or isinstance(help_for, dpy_commands.bot.BotBase):
            await self.format_bot_help(ctx)
            return

        if isinstance(help_for, str):
            try:
                help_for = self.parse_command(ctx, help_for)
            except NoCommand:
                await self.command_not_found(ctx, help_for)
                return
            except NoSubCommand as exc:
                if self.CONFIRM_UNAVAILABLE_COMMAND_EXISTENCES:
                    await self.subcommand_not_found(ctx, exc.last, exc.not_found)
                    return
                help_for = exc.last

        if isinstance(help_for, commands.Cog):
            await self.format_cog_help(ctx, help_for)
        else:
            await self.format_command_help(ctx, help_for)

    async def get_cog_help_mapping(self, ctx: Context, obj: commands.Cog):
        iterator = filter(lambda c: c.parent is None and c.cog is obj, ctx.bot.commands)
        return {com.name: com async for com in self.help_filter_func(ctx, iterator)}

    async def get_group_help_mapping(self, ctx: Context, obj: commands.Group):
        return {
            com.name: com async for com in self.help_filter_func(ctx, obj.all_commands.values())
        }

    async def get_bot_help_mapping(self, ctx):
        sorted_iterable = []
        for cogname, cog in (*sorted(ctx.bot.cogs.items()), (None, None)):
            cm = await self.get_cog_help_mapping(ctx, cog)
            if cm:
                sorted_iterable.append((cogname, cm))
        return sorted_iterable

    @staticmethod
    def get_default_tagline(ctx: Context):
        return (
            f"Type {ctx.clean_prefix}help <command> for more info on a command. "
            f"You can also type {ctx.clean_prefix}help <category> for more info on a category."
        )

    async def format_command_help(self, ctx: Context, obj: commands.Command):

        send = self.CONFIRM_UNAVAILABLE_COMMAND_EXISTENCES
        if not send:
            async for _ in self.help_filter_func(ctx, (obj,), bypass_hidden=True):
                # This is a really lazy option for not
                # creating a separate single case version.
                # It is efficient though
                #
                # We do still want to bypass the hidden requirement on
                # a specific command explicitly invoked here.
                send = True

        if not send:
            return

        command = obj

        description = command.description or ""
        tagline = (await ctx.bot.db.help.tagline()) or self.get_default_tagline(ctx)
        signature = f"`Syntax: {ctx.clean_prefix}{command.qualified_name} {command.signature}`"
        subcommands = None

        if hasattr(command, "all_commands"):
            grp = cast(commands.Group, command)
            subcommands = await self.get_group_help_mapping(ctx, grp)

        if await ctx.embed_requested():
            emb = {"embed": {"title": "", "description": ""}, "footer": {"text": ""}, "fields": []}

            if description:
                emb["embed"]["title"] = f"*{description[:2044]}*"

            emb["footer"]["text"] = tagline
            emb["embed"]["description"] = signature

            if command.help:
                splitted = command.help.split("\n\n")
                name = "__{0}__".format(splitted[0])
                value = "\n\n".join(splitted[1:]).replace("[p]", ctx.clean_prefix)
                if not value:
                    value = EMPTY_STRING
                field = EmbedField(name[:252], value[:1024], False)
                emb["fields"].append(field)

            if subcommands:
                subtext = "\n".join(
                    f"**{name}** {command.short_doc}"
                    for name, command in sorted(subcommands.items())
                )
                for i, page in enumerate(pagify(subtext, page_length=1000, shorten_by=0)):
                    if i == 0:
                        title = "**__Subcommands:__**"
                    else:
                        title = "**__Subcommands:__** (continued)"
                    field = EmbedField(title, page, False)
                    emb["fields"].append(field)

            await self.make_and_send_embeds(ctx, emb)

        else:  # Code blocks:

            subtext = None
            subtext_header = None
            if subcommands:
                subtext_header = "Subcommands:"
                max_width = max(discord.utils._string_width(name) for name in subcommands.keys())

                def width_maker(cmds):
                    doc_max_width = 80 - max_width
                    for nm, com in sorted(cmds):
                        width_gap = discord.utils._string_width(nm) - len(nm)
                        doc = command.short_doc
                        if len(doc) > doc_max_width:
                            doc = doc[: doc_max_width - 3] + "..."
                        yield nm, doc, max_width - width_gap

                subtext = "\n".join(
                    f"  {name:<{width}} {doc}"
                    for name, doc, width in width_maker(subcommands.items())
                )

            to_page = "\n\n".join(
                filter(None, (description, signature[1:-1], command.help, subtext_header, subtext))
            )
            pages = [box(p) for p in pagify(to_page)]
            await self.send_pages(ctx, pages, embed=False)

    @staticmethod
    def group_embed_fields(fields: List[EmbedField], max_chars=1000):
        curr_group = []
        ret = []
        for f in fields:
            curr_group.append(f)
            if sum(len(f.value) for f in curr_group) > max_chars:
                ret.append(curr_group)
                curr_group = []

        if len(curr_group) > 0:
            ret.append(curr_group)

        return ret

    async def make_and_send_embeds(self, ctx, embed_dict: dict):

        pages = []

        page_char_limit = await ctx.bot.db.help.page_char_limit()
        field_groups = self.group_embed_fields(embed_dict["fields"], page_char_limit)

        color = await ctx.embed_color()
        page_count = len(field_groups)

        author_info = {"name": f"{ctx.me.display_name} Help Menu", "icon_url": ctx.me.avatar_url}

        for i, group in enumerate(field_groups, 1):
            embed = discord.Embed(color=color, **embed_dict["embed"])

            if page_count > 1:
                description = f"{embed.description} *Page {i} of {page_count}*"
                embed.description = description

            embed.set_author(**author_info)

            for field in group:
                embed.add_field(**field._asdict())

            embed.set_footer(**embed_dict["footer"])

            pages.append(embed)

        await self.send_pages(ctx, pages, embed=True)

    async def format_cog_help(self, ctx: Context, obj: commands.Cog):

        commands = await self.get_cog_help_mapping(ctx, obj)
        if not (commands or self.CONFIRM_UNAVAILABLE_COMMAND_EXISTENCES):
            return

        description = obj.help
        tagline = (await ctx.bot.db.help.tagline()) or self.get_default_tagline(ctx)

        if await ctx.embed_requested():
            emb = {"embed": {"title": "", "description": ""}, "footer": {"text": ""}, "fields": []}

            emb["footer"]["text"] = tagline
            if description:
                emb["embed"]["title"] = f"*{description[:2044]}*"

            if commands:
                command_text = "\n".join(
                    f"**{name}** {command.short_doc}" for name, command in sorted(commands.items())
                )
                for i, page in enumerate(pagify(command_text, page_length=1000, shorten_by=0)):
                    if i == 0:
                        title = "**__Commands:__**"
                    else:
                        title = "**__Commands:__** (continued)"
                    field = EmbedField(title, page, False)
                    emb["fields"].append(field)

            await self.make_and_send_embeds(ctx, emb)

        else:
            commands_text = None
            commands_header = None
            if commands:
                subtext_header = "Commands:"
                max_width = max(discord.utils._string_width(name) for name in commands.keys())

                def width_maker(cmds):
                    doc_max_width = 80 - max_width
                    for nm, com in sorted(cmds):
                        width_gap = discord.utils._string_width(nm) - len(nm)
                        doc = com.short_doc
                        if len(doc) > doc_max_width:
                            doc = doc[: doc_max_width - 3] + "..."
                        yield nm, doc, max_width - width_gap

                subtext = "\n".join(
                    f"  {name:<{width}} {doc}"
                    for name, doc, width in width_maker(commands.items())
                )

            to_page = "\n\n".join(
                filter(None, (description, signature[1:-1], subtext_header, subtext))
            )
            pages = [box(p) for p in pagify(to_page)]
            await self.send_pages(ctx, pages, embed=False)

    async def format_bot_help(self, ctx: Context):

        commands = await self.get_bot_help_mapping(ctx)
        if not commands:
            return

        description = ctx.bot.description or ""
        tagline = (await ctx.bot.db.help.tagline()) or self.get_default_tagline(ctx)

        if await ctx.embed_requested():

            emb = {"embed": {"title": "", "description": ""}, "footer": {"text": ""}, "fields": []}

            emb["footer"]["text"] = tagline
            if description:
                emb["embed"]["title"] = f"*{description[:2044]}*"

            for cog_name, data in commands:

                if cog_name:
                    title = f"**__{cog_name}:__**"
                else:
                    title = f"**__No Category:__**"

                cog_text = "\n".join(
                    f"**{name}** {command.short_doc}" for name, command in sorted(data.items())
                )

                for i, page in enumerate(pagify(cog_text, page_length=1000, shorten_by=0)):
                    title = title if i < 1 else f"{title} (continued)"
                    field = EmbedField(title, page, False)
                    emb["fields"].append(field)

            await self.make_and_send_embeds(ctx, emb)

        else:
            if description:
                to_join = [f"{description}\n"]

            names = []
            for k, v in commands:
                names.extend(list(v.name for v in v.values()))

            max_width = max(
                discord.utils._string_width((name or "No Category:")) for name in names
            )

            def width_maker(cmds):
                doc_max_width = 80 - max_width
                for nm, com in cmds:
                    width_gap = discord.utils._string_width(nm) - len(nm)
                    doc = com.short_doc
                    if len(doc) > doc_max_width:
                        doc = doc[: doc_max_width - 3] + "..."
                    yield nm, doc, max_width - width_gap

            for cog_name, data in commands:

                title = f"{cog_name}:" if cog_name else "No Category:"
                to_join.append(title)

                for name, doc, width in width_maker(sorted(data.items())):
                    to_join.append(f"  {name:<{width}} {doc}")

            to_join.append(f"\n{tagline}")
            to_page = "\n".join(to_join)
            pages = [box(p) for p in pagify(to_page)]
            await self.send_pages(ctx, pages, embed=False)

    async def help_filter_func(
        self, ctx, objects: Iterable[SupportsCanSee], bypass_hidden=False
    ) -> AsyncIterator[SupportsCanSee]:
        """
        This does most of actual filtering.
        """
        # TODO: Settings for this in core bot db
        for obj in objects:
            if self.VERIFY_CHECKS and not (self.SHOW_HIDDEN or bypass_hidden):
                # Default Red behavior, can_see includes a can_run check.
                if await obj.can_see(ctx):
                    yield obj
            elif self.VERIFY_CHECKS:
                if await obj.can_run(ctx):
                    yield obj
            elif not (self.SHOW_HIDDEN or bypass_hidden):
                if getattr(obj, "hidden", False):  # Cog compatibility
                    yield obj
            else:
                yield obj

    async def command_not_found(self, ctx, help_for):
        """
        Sends an error, fuzzy help, or stays quiet based on settings
        """
        coms = [c async for c in self.help_filter_func(ctx, ctx.bot.walk_commands())]
        fuzzy_commands = await fuzzy_command_search(ctx, help_for, commands=coms, min_score=75)
        use_embeds = await ctx.embed_requested()
        if fuzzy_commands:
            ret = await format_fuzzy_results(ctx, fuzzy_commands, embed=use_embeds)
            if use_embeds:
                ret.set_author()
                tagline = (await ctx.bot.db.help.tagline()) or self.get_default_tagline(ctx)
                ret.set_footer(text=tagline)
                await ctx.send(embed=ret)
            else:
                await ctx.send(ret)
        elif self.CONFIRM_UNAVAILABLE_COMMAND_EXISTENCES:
            ret = T_("Command *{command_name}* not found.").format(command_name=command_name)
            if use_embeds:
                emb = discord.Embed(color=(await ctx.embed_color()), description=ret)
                emb.set_author(name=f"{ctx.me.display_name} Help Menu", icon_url=ctx.me.avatar_url)
                tagline = (await ctx.bot.db.help.tagline()) or self.get_default_tagline(ctx)
                ret.set_footer(text=tagline)
                await ctx.send(embed=ret)
            else:
                await ctx.send(ret)

    async def subcommand_not_found(self, ctx, command, not_found):
        """
        Sends an error
        """
        ret = T_("Command *{command_name}* has no subcommands.").format(
            command_name=command.qualified_name
        )
        await ctx.send(ret)

    @staticmethod
    def parse_command(ctx, help_for: str):
        """
        Handles parsing
        """

        maybe_cog = ctx.bot.get_cog(help_for)
        if maybe_cog:
            return maybe_cog

        com = ctx.bot
        last = None

        clist = help_for.split()

        for index, item in enumerate(clist):
            try:
                com = com.all_commands[item]
                # TODO: This doesn't handle valid command aliases.
                # swap parsing method to use get_command.
            except (KeyError, AttributeError):
                if last:
                    raise NoSubCommand(last=last, not_found=clist[index:]) from None
                else:
                    raise NoCommand() from None
            else:
                last = com

        return com

    async def send_pages(
        self, ctx: Context, pages: List[Union[str, discord.Embed]], embed: bool = True
    ):
        """
        Sends pages based on settings.
        """

        if not self.USE_MENU:

            max_pages_in_guild = await ctx.bot.db.help.max_pages_in_guild()
            destination = ctx.author if len(pages) > max_pages_in_guild else ctx

            if embed:
                for page in pages:
                    await destination.send(embed=page)
            else:
                for page in pages:
                    await destination.send(page)
        else:
            await menus.menu(ctx, pages, menus.DEFAULT_CONTROLS)


@commands.command(name="help", hidden=True, i18n=T_)
async def red_help(ctx: Context, *, thing_to_get_help_for: str = None):
    """
    I need somebody
    (Help) not just anybody
    (Help) you know I need someone
    (Help!)
    """
    await ctx.bot.send_help_for(ctx, thing_to_get_help_for)
