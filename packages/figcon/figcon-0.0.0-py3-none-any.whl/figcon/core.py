"""
Class for handling options.
"""
import inspect
from typing import Union, Optional
from importlib._bootstrap import module_from_spec
from importlib._bootstrap_external import spec_from_file_location
from pathlib import Path


_path_directives = {'primary', 'secondary', 'default'}


class Figcon:
    """ Class for handling finding and loading options """

    def __init__(self,
                 default_path: Union[str, Path],
                 primary_path: Optional[Union[str, Path]] = None,
                 secondary_path: Optional[Union[str, Path]] = None,
                 config_name='config.py'
                 ):
        """
        Create an options object.

        The order of precedent is primary -> secondary -> default.

        Parameters
        ----------
        default_path
            The path used for the default parameters.
        primary_path
            The path used for primary parameters. If not specified use cwd.
        secondary_path
            The path used for secondary parameters. If not specified use home.
        config_name
            The name of the config files that can be found in primary,
            secondary, or default paths.
        """
        # create a dict for storing state
        self.__state = {}
        # set paths
        self.default_path = default_path
        self.primary_path = primary_path or Path.cwd()
        self.secondary_path = secondary_path or Path.home()
        self._config_file_name = config_name
        # update state
        self.update_options()

    def __getattr__(self, item):
        """
        Try to get the attribute, first from primary, then secondary, then default.
        """
        try:
            return self.__state[item]
        except KeyError:
            msg = (
                f"Options contains no item {item}. You can set it in "
                f"a {self._config_file_name} file in either {self.default_path},"
                f" {self.primary_path} or {self.secondary_path}."
            )
            raise AttributeError(msg)

    def _update_defaults(self, new, base=None):
        """
        Try to intelligently update the base state, recursing into
        identically named objects with __dict__ and updating.

        This is a little complex, but seems to work so far...
        """
        base = base or self.__state
        # handle objects not already in instance state
        disjoint = set(new) - set(base)
        base.update({x: new[x] for x in disjoint})
        # handle overlaps
        overlap = set(base) & set(new)
        for item in overlap:
            obj1, obj2 = base[item], new[item]
            if inspect.isfunction(obj2):
                base[item] = obj2
            elif hasattr(obj2, "__dict__") and hasattr(obj1, "__dict__"):
                if obj1 is not obj2:
                    self._update_defaults(obj2.__dict__, obj1.__dict__)
            else:
                base[item] = obj2

    def _load_config(self, path: Union[str, Path], file_name: Optional[str]=None):
        """ load a parameter from the config model """
        file_name = file_name or self._config_file_name
        path = Path(path)
        # If a directory was provided look for expected file
        if path.is_dir():
            expected = Path(path) / file_name
            # if file not found look for hidden
            if not expected.exists() and not file_name.startswith('.'):
                expected = Path(path / ("." + file_name))
            if not expected.exists():
                return {}
            mod = file_name.replace(".py", "")
        # If a path to a file was passed
        elif path.is_file():
            expected = path
            mod = expected.name.replace(".py", "")
        # Get the spec and import module
        spec = spec_from_file_location(mod, expected)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        # pull out imported stuff and return the rest
        out = {}
        for item, value in mod.__dict__.items():
            # skip other modules or built-in stuff
            if inspect.ismodule(value) or item.startswith("__"):
                continue
            # skip classes defined in other modules
            if getattr(value, "__module__", mod.__name__) != mod.__name__:
                continue
            out[item] = value
        return out

    def update_options(self, primary_path=None, secondary_path=None):
        """
        Refresh the attributes to pull options from.

        Parameters
        ----------
        primary_path
            The directory of, or path to, the primary sconfig. If None use
            the current working directory.
        secondary_path
            The directory of, or path to, the secondary sconfig. If None use
            the user's home directory.

        Notes
        -----
        If a directory is supplied the top level of the directory is scanned
        for the expected filename. If None is found an exception is raised.
        """
        self.__state.clear()
        # define base, home, cwd (last takes priority)
        dirs = {
            'default': self.default_path,
            'secondary': Path(secondary_path or self.secondary_path),
            'primary': Path(primary_path or self.primary_path),
        }
        for directive, path in dirs.items():  # iterate locations and load, update state
            self._update_defaults(self._load_config(path))

    def set_option(self, **kwargs):
        """
        Set an option using the option as the key.

        Examples
        --------
        from ficcon import Figcon
        config = Figcon()
        config.set_option('bob', 'ham')
        assert config.bob == 'ham'

        """
        self.__state.update(**kwargs)

    def __delattr__(self, item):
        """
        Delete an option.
        """
        self.__state.pop(item, None)
