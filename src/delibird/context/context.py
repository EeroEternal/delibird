"""Context management for Delibird."""

from contextvars import ContextVar, Token


class Context:
    """Context class to manage the context of the application."""

    def __init__(self, name: str = None):
        # Context name in async context
        self.name: ContextVar = ContextVar(name or self.__class__.__name__)
        self._token: Token = self.name.set(self)

    def __enter__(self):
        """Enter the context."""
        return self

    def __exit__(self, *_):
        """Exit the context."""
        if not self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context exit called without an enter."
            )
        self.name.reset(self._token)
