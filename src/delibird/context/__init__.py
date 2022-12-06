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

# Set generic type
T = TypeVar("T")


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
