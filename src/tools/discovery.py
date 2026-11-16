from pkgutil import iter_modules
from types import ModuleType
from typing import Any

class ExtensionManager:
    """Manages extension discovery for Python packages.

    Attributes
    -----------
    extensions: Optional[:class:`int`]
        The number of extensions found by the most recent call to
        :meth:`discover_extensions`. This is ``None`` before discovery.
    """

    def __init__(self) -> None:
        self.extensions: int | None = None

    @property
    def extension_count(self) -> int:
        """:class:`int`: The number of extensions found during the most recent discovery.

        Raises
        -------
        RuntimeError
            Extension discovery has not been performed yet.
        """
        if self.extensions is not None:
            return self.extensions

        raise RuntimeError("Extension discovery has not been performed yet.")

    def discover_extensions(self, package: ModuleType) -> list[str]:
        """Finds extension module names in a Python package.

        Only direct child modules and subpackages are included. Names starting
        with an underscore are ignored. Subpackages are not searched recursively,
        and a ``setup`` entry point is not required.

        This updates :attr:`extensions` with the number of names found.

        Parameters
        -----------
        package: :class:`py:types.ModuleType`
            The imported Python package to search.

        Raises
        -------
        TypeError
            The argument is not a module, or its ``__path__`` attribute is
            missing or ``None``.

        Returns
        --------
        List[:class:`str`]
            The fully qualified names of the discovered modules and subpackages,
            sorted alphabetically.
        """
        if not isinstance(package, ModuleType):
            raise TypeError("package must be a Python module")

        paths: Any | None = getattr(package, "__path__", None)

        if paths is None:
            raise TypeError("package must be a Python package")

        sync: list[str] = sorted(
            module.name
            for module in iter_modules(
                paths,
                prefix=f"{package.__name__}.",
            )
            if not module.name.rsplit(".", 1)[-1].startswith("_")
        )

        self.extensions = len(sync)

        return sync
