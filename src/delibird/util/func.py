"""Function tools."""

from inspect import signature


def get_parameters(func, *args, **kwargs):
    """Get parameters of function.

    Args:
        func: function to get parameters
        *args: arguments
        **kwargs: keyword arguments
    Returns:
        OrderedDict[str, Any]: parameters
    """
    sig = signature(func)
    return sig.bind(*args, **kwargs).arguments
