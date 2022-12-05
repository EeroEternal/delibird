"""Context management for Delibird."""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ContextManager,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from contextvars import ContextVar, Token


class Context:
    """Context class to manage the context of the application."""

    # ContextVar to store the current context in async environments
    _var: ContextVar
    _token: Token = None

    def __enter__(self):
        if self._token is not None:
            raise RuntimeError(
                "Context already entered. Context enter calls cannot be nested."
            )
        self._token = self._var.set(self)
        return self

    def __exit__(self, *_):
        if not self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context exit called without an enter."
            )
        self._var.reset(self._token)
        self._token = None

    @classmethod
    def get(cls: Type[T]) -> Optional[T]:
        return cls.__var__.get(None)

    def copy(self, **kwargs):
        """
        Duplicate the context model, optionally choosing which fields to include, exclude, or change.

        Attributes:
            include: Fields to include in new model.
            exclude: Fields to exclude from new model, as with values this takes precedence over include.
            update: Values to change/add in the new model. Note: the data is not validated before creating
                the new model - you should trust this data.
            deep: Set to `True` to make a deep copy of the model.

        Returns:
            A new model instance.
        """
        # Remove the token on copy to avoid re-entrance errors
        new = super().copy(**kwargs)
        new._token = None
        return new
