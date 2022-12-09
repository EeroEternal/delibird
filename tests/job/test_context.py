"""Test env management."""

from contextvars import ContextVar, Token


class Context:
    """Context class to manage the env of the application.

    forbid mutation while providing a env manager with contextvar
    """

    # static element belongs to class
    __var__: ContextVar
    _token: Token

    def __int__(self):
        """Get the env instance."""
        print('env init')

    def __enter__(self):
        """Enter the env."""
        if self._token:
            raise RuntimeError(
                "Asymmetric use of env. Context enter called without an exit."
            )

        print('enter env')
        # env enter will return env instance with a token
        self._token = self.__var__.set(self)
        return self

    def __exit__(self, *_):
        """Exit the env."""
        if not self._token:
            raise RuntimeError(
                "Asymmetric use of env. Context exit called without an enter."
            )
        # Reset the env variable to the value it had before the
        # ContextVar.set() that created the token was used.
        self.__var__.reset(self._token)

        # reset token
        self._token = Token()

        print('exit env')

    @classmethod
    def get(cls):
        """Get the env instance."""
        print("get env")
        return cls.__var__.get()

    @classmethod
    def register(cls, class_):
        """Register the env."""
        class_init = class_.__init__
        print('register decorator')

        def __wrap_init__(self, *args, **kwargs):
            """Initialize the env."""
            print("init test env")
            class_init(self, *args, **kwargs)
            self.wrap_name = "register"

        class_.__init__ = __wrap_init__
        return class_


@Context.register
# pylint: disable=too-few-public-methods
class TestContext:
    """Test env management."""
    __test__ = False

    def test_context(self):
        """Test env."""
        print('test env method')


def test_context():
    """Test env."""
    context = TestContext()

    context.test_context()


# for print decorator. use python tests/workflow/test_context.py
if __name__ == '__main__':
    test_context()
