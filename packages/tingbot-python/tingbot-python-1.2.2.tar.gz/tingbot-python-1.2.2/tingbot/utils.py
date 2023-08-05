
class Struct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class CallbackList(object):
    def __init__(self):
        self._list = []

    def __call__(self):
        for callback in self._list:
            callback()

    def add(self, callback):
        self._list.append(callback)

    def copy(self):
        obj = CallbackList()
        obj._list = self._list[:]
        return obj


# cached_property from werkzeug
_missing = object()

class cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dict__` in order for this property to
    work.
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__.
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


class only_call_once(object):
    '''
    A function decorator that only calls the wrapped function once. Subsequent calls do nothing.
    '''
    def __init__(self, func):
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.func = func
        self.has_run = False

    def __call__(self):
        if not self.has_run:
            self.func()
            self.has_run = True


def call_with_optional_arguments(func, **kwargs):
    '''
    calls a function with the arguments **kwargs, but only those that the function defines.
    e.g.

    def fn(a, b):
        print a, b

    call_with_optional_arguments(fn, a=2, b=3, c=4)  # because fn doesn't accept `c`, it is discarded
    '''

    import inspect
    function_arg_names = inspect.getargspec(func).args

    for arg in kwargs.keys():
        if arg not in function_arg_names:
            del kwargs[arg]

    func(**kwargs)


def get_resource(name):
    '''
    Returns the path to a resource bundled in this library (at tingbot/resources/<name>)
    '''
    import os
    return os.path.join(os.path.dirname(__file__), 'resources', name)


import warnings


class deprecated(object):
    '''
    Decorates ("marks") a callable as deprecated.

    Example:

        @deprecated('Use after instead', version='1.1.0')
        def once():
            pass
    '''
    def __init__(self, message, version=''):
        self.message = message
        self.version = version

    def __call__(self, func):
        return deprecated_callable(func, message=self.message, version=self.version)


def deprecated_callable(func, version, message='', name=None):
    '''
    Returns a function that will warn the caller when called, but otherwise 
    work as normal.
    '''

    def deprecated_callable_inner(*args, **kwargs):
        warnings.warn(
            '{func_name} is deprecated (since {version}). {message}'.format(
                func_name=name or func.__name__,
                version=version,
                message=message),
            DeprecationWarning,
            stacklevel=2)

        return func(*args, **kwargs)

    return deprecated_callable_inner
