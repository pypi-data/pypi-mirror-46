# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


"""Use context managers with a function instead of a statement.

Provides a minimal, clean and portable interface for using context
managers with all the advantages of functions over syntax.
"""

import sys as _sys


__all__ = ('with_',)
__version__ = '1.0.1'


def with_(manager, action):
    """Execute an action within the scope of a context manager.

    Arguments:
        manager (ContextManager): The context manager instance to use.
        action (Callable[Any, Any]): The action to execute. Must accept
            the `as` value of the context manager as the first and only
            positional argument.

    Returns:
        Any: Return value of the executed action.
        None: If the manager suppresses an exception from the action.

    Raises:
        AttributeError: If the manager does not implement the
            ``__exit__`` or ``__enter__`` methods.
        Any: Exception raised by the executed action if the manager
            does not suppress it.
    """
    exit = type(manager).__exit__
    value = type(manager).__enter__(manager)
    try:
        result = action(value)
    except:
        if not exit(manager, *_sys.exc_info()):
            raise
        return None
    exit(manager, None, None, None)
    return result
