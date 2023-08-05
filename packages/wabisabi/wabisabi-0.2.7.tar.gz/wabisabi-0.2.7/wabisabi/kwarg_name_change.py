"""
As this library is still in early development, the API might change.
I suggest you vendor this so that you don't create conflicts if other
libraries decide to use an older, incompatible version

If you are shipping python source code, then I've included the license
at the bottom of this file to make your life easier.
"""

from distutils.version import LooseVersion as Version
from functools import wraps
import inspect
from warnings import warn
from .merge_docstrings import merge_docstrings

# Keep the order of params as is,
# `previous_arg_order` and `keep_old_signature`
# should be optional positional args.
def kwarg_name_change(version, previous_kwarg_map=None,
                      library_name=None, current_library_version=None):
    """A decorator factory for keyword arguments to be specified by their old names.

    If the current library version is smaller than version in which the new
    signature takes effect, this deprecator will:

    Issue a warnign pointing to the user's code if they call a function with
    too many positional arguments.

    Parameters
    ----------
    version: version-like
        Version in which the new function signature takes full effect.

    previous_kwarg_map: dictionary of kwarg name maps
        This dictionary contains the keys (the old kwarg names) and the
        associated values of the new kwarg names. You may specifiy as
        many kwarg name pairs as you wish.

    library_name: str
        Friendly library name to include in warning messages

    current_library_version: version-like
        The current version of the shipped library (typically your module's
        ``__version__``).

    Examples
    --------

    >>> from wabisabi import kwonly_change
    >>> import functools
    >>>
    >>> kwarg_name_change = functools.partial(kwarg_name_change,
    ...                                       library_name='my super lib',
    ...                                       current_library_version='0.14')
    >>> @kwarg_name_change('0.15', {'bar': 'foo'})
    ... def foo_new(zap='zip', *, foo='hello', baz='world'):
    ...     return zap + foo + baz

    """
    if current_library_version is None:
        raise ValueError('Must provide a version for your library.')

    if library_name is None:
        raise ValueError('You must provide a user friendly name for your '
                         'library.')

    def the_decorator(func):
        if Version(current_library_version) >= version:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            for key in kwargs.keys():
                if key in previous_kwarg_map:
                    new_key = previous_kwarg_map[key]
                    kwargs[new_key] = kwargs.pop(key)

                    warn("In version {version} of {library_name}, the "
                         "keyword argument: '{key}' will change names and "
                         "to be specified using the '{new_key}'."
                         "To suppress this warning, specify the keyword "
                         "argument with its new name."
                         "".format(
                            version=version, library_name=library_name,
                            key=key, new_key=new_key),
                         FutureWarning, stacklevel=2)

            return func(*args, **kwargs)

        # only add a docstring if they had one already
        if wrapper.__doc__ is None:
            return wrapper

        warnings_string = """
Warns
-----
FutureWarning
    In release {version} of {module}, the following keyword arguments can only
    be referred by their new names. For now, both names are accepted as valid:

""".format(version=version, module=library_name)

        for key, new_key in previous_kwarg_map.items():
            warnings_string += ("""
        '{new_key}' refers to the old keyword argument '{key}'"""
        "".format(new_key=new_key, key=key))

        warnings_string += """

    To avoid this warning, provide all the listed keyword arguments using their
    new names.

"""

        wrapper.__doc__ = merge_docstrings(wrapper, warnings_string)
        return wrapper
    return the_decorator


"""
BSD 3-Clause License

Copyright (c) 2019, Mark Harfouche
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
