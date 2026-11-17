from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import Any, ClassVar

class ExtensionManager:
    """Manages extension discovery for Python packages.

    Attributes
    ----------
    extensions : int or None
        The number of extensions found by the most recent call to
        `discover_extensions`, shared across instances of this class.
        This is ``None`` before discovery.
    """

    extensions: ClassVar[int | None] = None

    @property
    def extension_count(self) -> int:
        """Return the number of extensions found during the most recent discovery.

        Returns
        -------
        int
            The number of extensions found.

        Raises
        ------
        RuntimeError
            Extension discovery has not been performed yet.
        """
        if self.extensions is not None:
            return self.extensions

        raise RuntimeError("Extension discovery has not been performed yet.")

    @classmethod
    def discover_extensions(cls, *packages: ModuleType) -> list[str]:
        """Find extension module names in Python packages.

        Subpackages are imported and searched recursively, but are not included
        in the results. Names starting with an underscore are ignored, including
        their descendants. A ``setup`` entry point is not required.

        Subpackage imports execute their ``__init__.py`` files. Directories
        without ``__init__.py`` are not discovered by this traversal.

        This updates `extensions` with the total number of names found.
        With no packages, returns an empty list and sets the count to zero.

        Parameters
        ----------
        *packages : types.ModuleType
            The imported Python packages to search, in order.

        Returns
        -------
        list of str
            The fully qualified names of the discovered modules,
            sorted alphabetically within each package and combined in argument
            order.

        Raises
        ------
        TypeError
            An argument is not a module, or its ``__path__`` attribute is
            missing or ``None``.
        ImportError
            A subpackage cannot be imported. Other errors raised during
            subpackage initialization also propagate to the caller.
        """
        def discover(package: ModuleType) -> list[str]:
            if not isinstance(package, ModuleType):
                raise TypeError("package must be a Python module")

            paths: Any | None = getattr(package, "__path__", None)

            if paths is None:
                raise TypeError("package must be a Python package")

            discovered: list[str] = []
            for module in iter_modules(paths, prefix=f"{package.__name__}."):
                if module.name.rsplit(".", 1)[-1].startswith("_"):
                    continue

                if module.ispkg:
                    discovered.extend(discover(import_module(module.name)))
                else:
                    discovered.append(module.name)

            return discovered

        extensions: list[str] = []
        for package in packages:
            extensions.extend(sorted(discover(package)))

        cls.extensions = len(extensions)

        return extensions
