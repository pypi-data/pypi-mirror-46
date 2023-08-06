import asyncio
import inspect
import io,os,sys
import textwrap
import traceback
import re
from contextlib import redirect_stdout
from copy import copy
from pathlib import Path
import contextlib
import discord
from redbot.core import checks
from ... import commands
from redbot.core.utils.chat_formatting import box, pagify
from ...downloader import Downloader

START_CODE_BLOCK_RE = re.compile(r"^((```py)(?=\s)|(```))")

def _(a):
    return a

class Developer(Downloader,commands.Cog):
    """Various development focused utilities."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return START_CODE_BLOCK_RE.sub("", content)[:-3]

        # remove `foo`
        return content.strip("` \n")

    @staticmethod
    def get_syntax_error(e):
        """Format a syntax error to send to the user.

        Returns a string representation of the error formatted as a codeblock.
        """
        if e.text is None:
            return box("{0.__class__.__name__}: {0}".format(e), lang="py")
        return box("{0.text}{1:>{0.offset}}\n{2}: {0}".format(e, "^", type(e).__name__), lang="py")

    @staticmethod
    def get_pages(msg: str):
        """Pagify the given message for output to the user."""
        return pagify(msg, delims=["\n", " "], priority=True, shorten_by=10)

    @staticmethod
    def sanitize_output(ctx: commands.Context, input_: str) -> str:
        """Hides the bot's token from a string."""
        token = ctx.bot.http.token
        r = "[EXPUNGED]"
        result = input_.replace(token, r)
        result = result.replace(token.lower(), r)
        result = result.replace(token.upper(), r)
        return result

    @commands.command()
    @checks.is_owner()
    async def debug(self, ctx, *, code):
        """Evaluate a statement of python code.

        The bot will always respond with the return value of the code.
        If the return value of the code is a coroutine, it will be awaited,
        and the result of that will be the bot's response.

        Note: Only one statement may be evaluated. Using await, yield or
        similar restricted keywords will result in a syntax error. For multiple
        lines or asynchronous code, see [p]repl or [p]eval.

        Environment Variables:
            ctx      - command invokation context
            bot      - bot object
            channel  - the current channel object
            author   - command author's member object
            message  - the command's message object
            discord  - discord.py library
            commands - redbot.core.commands
            _        - The result of the last dev command.
        """
        env = {
            "bot": ctx.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "discord": discord,
            "commands": commands,
            "_": self._last_result,
        }

        code = self.cleanup_code(code)

        try:
            result = eval(code, env)
        except SyntaxError as e:
            await ctx.send(self.get_syntax_error(e))
            return
        except Exception as e:
            await ctx.send(box("{}: {!s}".format(type(e).__name__, e), lang="py"))
            return

        if asyncio.iscoroutine(result):
            result = await result

        self._last_result = result

        result = self.sanitize_output(ctx, str(result))

        await ctx.send_interactive(self.get_pages(result), box_lang="py")

    @commands.command(name="eval")
    @checks.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Execute asynchronous code.

        This command wraps code into the body of an async function and then
        calls and awaits it. The bot will respond with anything printed to
        stdout, as well as the return value of the function.

        The code can be within a codeblock, inline code or neither, as long
        as they are not mixed and they are formatted correctly.

        Environment Variables:
            ctx      - command invokation context
            bot      - bot object
            channel  - the current channel object
            author   - command author's member object
            message  - the command's message object
            discord  - discord.py library
            commands - redbot.core.commands
            _        - The result of the last dev command.
        """
        env = {
            "bot": ctx.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "discord": discord,
            "commands": commands,
            "_": self._last_result,
        }

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = "async def func():\n%s" % textwrap.indent(body, "  ")

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env["func"]
        result = None
        try:
            with redirect_stdout(stdout):
                result = await func()
        except:
            printed = "{}{}".format(stdout.getvalue(), traceback.format_exc())
        else:
            printed = stdout.getvalue()
            await ctx.tick()

        if result is not None:
            self._last_result = result
            msg = "{}{}".format(printed, result)
        else:
            msg = printed
        msg = self.sanitize_output(ctx, msg)

        await ctx.send_interactive(self.get_pages(msg), box_lang="py")

    @commands.command()
    @checks.is_owner()
    async def paths(self, ctx: commands.Context):
        """
        Lists current cog paths in order of priority.
        """
        cog_mgr = ctx.bot.cog_mgr
        install_path = await cog_mgr.install_path()
        core_path = cog_mgr.CORE_PATH
        cog_paths = await cog_mgr.user_defined_paths()

        msg = _("Install Path: {install_path}\nCore Path: {core_path}\n\n").format(
            install_path=install_path, core_path=core_path
        )

        partial = []
        for i, p in enumerate(cog_paths, start=1):
            partial.append("{}. {}".format(i, p))

        msg += "\n".join(partial)
        await ctx.send(box(msg))

    @commands.command()
    @checks.is_owner()
    async def addpath(self, ctx: commands.Context, path: Path):
        """
        Add a path to the list of available cog paths.
        """
        if not path.is_dir():
            await ctx.send(_("That path does not exist or does not point to a valid directory."))
            return

        try:
            await ctx.bot.cog_mgr.add_path(path)
        except ValueError as e:
            await ctx.send(str(e))
        else:
            await ctx.send(_("Path successfully added."))

    @commands.command()
    @checks.is_owner()
    async def removepath(self, ctx: commands.Context, path_number: int):
        """
        Removes a path from the available cog paths given the path_number
            from !paths
        """
        path_number -= 1
        if path_number < 0:
            await ctx.send(_("Path numbers must be positive."))
            return

        cog_paths = await ctx.bot.cog_mgr.user_defined_paths()
        try:
            to_remove = cog_paths.pop(path_number)
        except IndexError:
            await ctx.send(_("That is an invalid path number."))
            return

        await ctx.bot.cog_mgr.remove_path(to_remove)
        await ctx.send(_("Path successfully removed."))

    @commands.command()
    @checks.is_owner()
    async def reorderpath(self, ctx: commands.Context, from_: int, to: int):
        """
        Reorders paths internally to allow discovery of different cogs.
        """
        # Doing this because in the paths command they're 1 indexed
        from_ -= 1
        to -= 1
        if from_ < 0 or to < 0:
            await ctx.send(_("Path numbers must be positive."))
            return

        all_paths = await ctx.bot.cog_mgr.user_defined_paths()
        try:
            to_move = all_paths.pop(from_)
        except IndexError:
            await ctx.send(_("Invalid 'from' index."))
            return

        try:
            all_paths.insert(to, to_move)
        except IndexError:
            await ctx.send(_("Invalid 'to' index."))
            return

        await ctx.bot.cog_mgr.set_paths(all_paths)
        await ctx.send(_("Paths reordered."))

    @commands.command()
    @checks.is_owner()
    async def installpath(self, ctx: commands.Context, path: Path = None):
        """
        Returns the current install path or sets it if one is provided.
            The provided path must be absolute or relative to the bot's
            directory and it must already exist.

        No installed cogs will be transferred in the process.
        """
        if path:
            if not path.is_absolute():
                path = (ctx.bot.main_dir / path).resolve()
            try:
                await ctx.bot.cog_mgr.set_install_path(path)
            except ValueError:
                await ctx.send(_("That path does not exist."))
                return

        install_path = await ctx.bot.cog_mgr.install_path()
        await ctx.send(
            _("The bot will install new cogs to the `{}` directory.").format(install_path)
        )

    @commands.command()
    @checks.is_owner()
    async def cogs(self, ctx: commands.Context):
        """
        Lists all loaded and available cogs.
        """
        loaded = set(ctx.bot.extensions.keys())

        all_cogs = set(await ctx.bot.cog_mgr.available_modules())

        unloaded = all_cogs - loaded

        loaded = sorted(list(loaded), key=str.lower)
        unloaded = sorted(list(unloaded), key=str.lower)

        if await ctx.embed_requested():
            loaded = _("**{} loaded:**\n").format(len(loaded)) + ", ".join(loaded)
            unloaded = _("**{} unloaded:**\n").format(len(unloaded)) + ", ".join(unloaded)

            for page in pagify(loaded, delims=[", ", "\n"], page_length=1800):
                e = discord.Embed(description=page, colour=discord.Colour.dark_green())
                await ctx.send(embed=e)

            for page in pagify(unloaded, delims=[", ", "\n"], page_length=1800):
                e = discord.Embed(description=page, colour=discord.Colour.dark_red())
                await ctx.send(embed=e)
        else:
            loaded_count = _("**{} loaded:**\n").format(len(loaded))
            loaded = ", ".join(loaded)
            unloaded_count = _("**{} unloaded:**\n").format(len(unloaded))
            unloaded = ", ".join(unloaded)
            loaded_count_sent = False
            unloaded_count_sent = False
            for page in pagify(loaded, delims=[", ", "\n"], page_length=1800):
                if page.startswith(", "):
                    page = page[2:]
                if not loaded_count_sent:
                    await ctx.send(loaded_count + box(page, lang="css"))
                    loaded_count_sent = True
                else:
                    await ctx.send(box(page, lang="css"))

            for page in pagify(unloaded, delims=[", ", "\n"], page_length=1800):
                if page.startswith(", "):
                    page = page[2:]
                if not unloaded_count_sent:
                    await ctx.send(unloaded_count + box(page, lang="ldif"))
                    unloaded_count_sent = True
                else:
                    await ctx.send(box(page, lang="ldif"))

    @commands.command(name="restart")
    @checks.is_owner()
    async def _restart(self, ctx: commands.Context, silently: bool = False):
        """Attempts to restart ANBOT

        Makes ANBOT quit with exit code 26
        The restart is not guaranteed: it must be dealt
        with by the process manager in use"""
        with contextlib.suppress(discord.HTTPException):
            if not silently:
                await ctx.send(_("Restarting..."))
        os.system('clear')
        python = sys.executable
        os.execl(python, python, *sys.argv)
        await ctx.bot.shutdown(restart=True)

    @commands.command()
    @checks.is_owner()
    async def repl(self, ctx):
        """Open an interactive REPL.
        The REPL will only recognise code as messages which start with a
        backtick. This includes codeblocks, and as such multiple lines can be
        evaluated.
        You may not await any code in this REPL unless you define it inside an
        async function.
        """
        variables = {
            "ctx": ctx,
            "bot": ctx.bot,
            "message": ctx.message,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "author": ctx.author,
            "_": None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send(
                _("Already running a REPL session in this channel. Exit it with `quit`.")
            )
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send(_("Enter code to execute or evaluate. `exit()` or `quit` to exit."))

        msg_check = lambda m: (
            m.author == ctx.author and m.channel == ctx.channel and m.content.startswith("`")
        )

        while True:
            response = await ctx.bot.wait_for("message", check=msg_check)

            cleaned = self.cleanup_code(response.content)

            if cleaned in ("quit", "exit", "exit()"):
                await ctx.send("Exiting.")
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count("\n") == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, "<repl session>", "eval")
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, "<repl session>", "exec")
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables["message"] = response

            stdout = io.StringIO()

            msg = ""

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except:
                value = stdout.getvalue()
                msg = "{}{}".format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    msg = "{}{}".format(value, result)
                    variables["_"] = result
                elif value:
                    msg = "{}".format(value)

            msg = self.sanitize_output(ctx, msg)

            try:
                await ctx.send_interactive(self.get_pages(msg), box_lang="py")
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(_("Unexpected error: `{}`").format(e))