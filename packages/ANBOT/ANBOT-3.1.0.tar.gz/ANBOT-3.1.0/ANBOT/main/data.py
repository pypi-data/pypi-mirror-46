import contextlib
import pkgutil
from importlib import import_module, invalidate_caches
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import Union, List, Optional

import ANBOT.feature
from ..utils import deduplicate_iterables
import discord
from .config import Config
from .manage import cog_data_path

from ..utils.chat_formatting import box, pagify

__all__ = ["Data"]


class NoSuchCog(ImportError):
    """Thrown when a cog is missing.

    Different from ImportError because some ImportErrors can happen inside cogs.
    """


class Data:
    """Directory Data for ANBOT's cogs.

    This module allows you to load cogs from multiple directories and even from
    outside the bot directory. You may also set a directory for downloader to
    install new cogs to, the default being the :code:`cogs/` folder in the root
    bot directory.
    """

    CORE_PATH = Path(ANBOT.feature.__path__[0])

    def __init__(self):
        self.conf = Config.get_conf(self, 2938473984732, True)
        tmp_cog_install_path = cog_data_path(self) / "cogs"
        tmp_cog_install_path.mkdir(parents=True, exist_ok=True)
        self.conf.register_global(paths=[], install_path=str(tmp_cog_install_path))

    async def paths(self) -> List[Path]:
        """Get all currently valid path directories, in order of priority

        Returns
        -------
        List[pathlib.Path]
            A list of paths where cog packages can be found. The
            install path is highest priority, followed by the
            user-defined paths, and the core path has the lowest
            priority.

        """
        return deduplicate_iterables(
            [await self.install_path()], await self.user_defined_paths(), [self.CORE_PATH]
        )

    async def install_path(self) -> Path:
        """Get the install path for 3rd party cogs.

        Returns
        -------
        pathlib.Path
            The path to the directory where 3rd party cogs are stored.

        """
        return Path(await self.conf.install_path()).resolve()

    async def user_defined_paths(self) -> List[Path]:
        """Get a list of user-defined cog paths.

        All paths will be absolute and unique, in order of priority.

        Returns
        -------
        List[pathlib.Path]
            A list of user-defined paths.

        """
        return list(map(Path, deduplicate_iterables(await self.conf.paths())))

    async def set_install_path(self, path: Path) -> Path:
        """Set the install path for 3rd party cogs.

        Note
        ----
        The bot will not remember your old cog install path which means
        that **all previously installed cogs** will no longer be found.

        Parameters
        ----------
        path : pathlib.Path
            The new directory for cog installs.

        Returns
        -------
        pathlib.Path
            Absolute path to the new install directory.

        Raises
        ------
        ValueError
            If :code:`path` is not an existing directory.

        """
        if not path.is_dir():
            raise ValueError("The install path must be an existing directory.")
        resolved = path.resolve()
        await self.conf.install_path.set(str(resolved))
        return resolved

    @staticmethod
    def _ensure_path_obj(path: Union[Path, str]) -> Path:
        """Guarantee an object will be a path object.

        Parameters
        ----------
        path : `pathlib.Path` or `str`

        Returns
        -------
        pathlib.Path

        """
        try:
            path.exists()
        except AttributeError:
            path = Path(path)
        return path

    async def add_path(self, path: Union[Path, str]) -> None:
        """Add a cog path to current list.

        This will ignore duplicates.

        Parameters
        ----------
        path : `pathlib.Path` or `str`
            Path to add.

        Raises
        ------
        ValueError
            If :code:`path` does not resolve to an existing directory.

        """
        path = self._ensure_path_obj(path)

        # This makes the path absolute, will break if a bot install
        # changes OS/Computer?
        path = path.resolve()

        if not path.is_dir():
            raise ValueError("'{}' is not a valid directory.".format(path))

        if path == await self.install_path():
            raise ValueError("Cannot add the install path as an additional path.")
        if path == self.CORE_PATH:
            raise ValueError("Cannot add the core path as an additional path.")

        current_paths = await self.user_defined_paths()
        if path not in current_paths:
            current_paths.append(path)
            await self.set_paths(current_paths)

    async def remove_path(self, path: Union[Path, str]) -> None:
        """Remove a path from the current paths list.

        Parameters
        ----------
        path : `pathlib.Path` or `str`
            Path to remove.

        """
        path = self._ensure_path_obj(path).resolve()
        paths = await self.user_defined_paths()

        paths.remove(path)
        await self.set_paths(paths)

    async def set_paths(self, paths_: List[Path]):
        """Set the current paths list.

        Parameters
        ----------
        paths_ : `list` of `pathlib.Path`
            List of paths to set.

        """
        str_paths = list(map(str, paths_))
        await self.conf.paths.set(str_paths)

    async def _find_ext_cog(self, name: str) -> ModuleSpec:
        """
        Attempts to find a spec for a third party installed cog.

        Parameters
        ----------
        name : str
            Name of the cog package to look for.

        Returns
        -------
        importlib.machinery.ModuleSpec
            Module spec to be used for cog loading.

        Raises
        ------
        NoSuchCog
            When no cog with the requested name was found.

        """
        real_paths = list(map(str, [await self.install_path()] + await self.user_defined_paths()))

        for finder, module_name, _ in pkgutil.iter_modules(real_paths):
            if name == module_name:
                spec = finder.find_spec(name)
                if spec:
                    return spec

        raise NoSuchCog(
            "No 3rd party module by the name of '{}' was found in any available path.".format(
                name
            ),
            name=name,
        )

    @staticmethod
    async def _find_core_cog(name: str) -> ModuleSpec:
        """
        Attempts to find a spec for a core cog.

        Parameters
        ----------
        name : str

        Returns
        -------
        importlib.machinery.ModuleSpec

        Raises
        ------
        RuntimeError
            When no matching spec can be found.
        """
        real_name = ".{}".format(name)
        package = "ANBOT.feature"

        try:
            mod = import_module(real_name, package=package)
        except ImportError as e:
            if e.name == package + real_name:
                raise NoSuchCog(
                    "No core cog by the name of '{}' could be found.".format(name),
                    path=e.path,
                    name=e.name,
                ) from e

            raise

        return mod.__spec__

    # noinspection PyUnreachableCode
    async def find_cog(self, name: str) -> Optional[ModuleSpec]:
        """Find a cog in the list of available paths.

        Parameters
        ----------
        name : str
            Name of the cog to find.

        Returns
        -------
        Optional[importlib.machinery.ModuleSpec]
            A module spec to be used for specialized cog loading, if found.

        """
        with contextlib.suppress(NoSuchCog):
            return await self._find_ext_cog(name)

        with contextlib.suppress(NoSuchCog):
            return await self._find_core_cog(name)

    async def available_modules(self) -> List[str]:
        """Finds the names of all available modules to load."""
        paths = list(map(str, await self.paths()))

        ret = []
        for finder, module_name, _ in pkgutil.iter_modules(paths):
            ret.append(module_name)
        return ret

    @staticmethod
    def invalidate_caches():
        """Re-evaluate modules in the py cache.

        This is an alias for an importlib internal and should be called
        any time that a new module has been installed to a cog directory.
        """
        invalidate_caches()