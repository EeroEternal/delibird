"""Test context management."""

from contextvars import ContextVar, Token


class Context:
    """Context class to manage the context of the application.

    forbid mutation while providing a context manager with contextvar
    """

    # static element belongs to class
    __var__: ContextVar
    _token: Token

    def __int__(self):
        """Get the context instance."""
        print('context init')

    def __enter__(self):
        """Enter the context."""
        if self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context enter called without an exit."
            )

        print('enter context')
        # context enter will return context instance with a token
        self._token = self.__var__.set(self)
        return self

    def __exit__(self, *_):
        """Exit the context."""
        if not self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context exit called without an enter."
            )
        # Reset the context variable to the value it had before the
        # ContextVar.set() that created the token was used.
        self.__var__.reset(self._token)

        # reset token
        self._token = Token()

        print('exit context')

    @classmethod
    def get(cls):
        """Get the context instance."""
        print("get context")
        return cls.__var__.get()

    @classmethod
    def register(cls, class_):
        """Register the context."""
        class_init = class_.__init__
        print('register decorator')

        def __wrap_init__(self, *args, **kwargs):
            """Initialize the context."""
            print("init test context")
            class_init(self, *args, **kwargs)
            self.wrap_name = "register"

        class_.__init__ = __wrap_init__
        return class_


@Context.register
# pylint: disable=too-few-public-methods
class TestContext:
    """Test context management."""
    __test__ = False

    def test_context(self):
        """Test context."""
        print('test context method')


def test_context():
    """Test context."""
    context = TestContext()

    context.test_context()


# for print decorator. use python tests/workflow/test_context.py
if __name__ == '__main__':
    test_context()
