import collections
import sys
import types


py2k = sys.version_info < (3, 0)
py3k = sys.version_info >= (3, 0)
py32 = sys.version_info >= (3, 2)
py27 = sys.version_info >= (2, 7)

if py3k:
    # Create constants for the compiler flags in Include/code.h
    # We try to get them from dis to avoid duplication, but fall
    # back to hardcoding so the dependency is optional
    try:
        from dis import COMPILER_FLAG_NAMES as _flag_names
    except ImportError:
        CO_OPTIMIZED, CO_NEWLOCALS = 0x1, 0x2
        CO_VARARGS, CO_VARKEYWORDS = 0x4, 0x8
        CO_NESTED, CO_GENERATOR, CO_NOFREE = 0x10, 0x20, 0x40
    else:
        mod_dict = globals()
        for k, v in _flag_names.items():
            mod_dict["CO_" + v] = k

    # See Include/object.h
    TPFLAGS_IS_ABSTRACT = 1 << 20

    Arguments = collections.namedtuple(
        "Arguments", ["args", "varargs", "varkw"]
    )
    ArgSpec = collections.namedtuple(
        "ArgSpec", ["args", "varargs", "keywords", "defaults"]
    )
    FullArgSpec = collections.namedtuple(
        "FullArgSpec",
        [
            "args",
            "varargs",
            "varkw",
            "defaults",
            "kwonlyargs",
            "kwonlydefaults",
            "annotations",
        ],
    )

    def ismethod(object):
        """Return true if the object is an instance method.
    
        Instance method objects provide these attributes:
            __doc__         documentation string
            __name__        name with which this method was defined
            __func__        function object containing implementation of method
            __self__        instance to which this method is bound"""
        return isinstance(object, types.MethodType)

    def isfunction(object):
        """Return true if the object is a user-defined function.
    
        Function objects provide these attributes:
            __doc__         documentation string
            __name__        name with which this function was defined
            __code__        code object containing compiled function bytecode
            __defaults__    tuple of any default values for arguments
            __globals__     global namespace in which this function was defined
            __annotations__ dict of parameter annotations
            __kwdefaults__  dict of keyword only parameters with defaults"""
        return isinstance(object, types.FunctionType)

    def iscode(object):
        """Return true if the object is a code object.
    
        Code objects provide these attributes:
            co_argcount     number of arguments (not including * or ** args)
            co_code         string of raw compiled bytecode
            co_consts       tuple of constants used in the bytecode
            co_filename     name of file in which this code object was created
            co_firstlineno  number of first line in Python source code
            co_flags        bitmap: 1=optimized | 2=newlocals | 4=*arg | 8=**arg
            co_lnotab       encoded mapping of line numbers to bytecode indices
            co_name         name with which this code object was defined
            co_names        tuple of names of local variables
            co_nlocals      number of local variables
            co_stacksize    virtual machine stack space required
            co_varnames     tuple of names of arguments and local variables"""
        return isinstance(object, types.CodeType)

    def _getfullargs(co):
        """Get information about the arguments accepted by a code object.
    
        Four things are returned: (args, varargs, kwonlyargs, varkw), where
        'args' and 'kwonlyargs' are lists of argument names, and 'varargs'
        and 'varkw' are the names of the * and ** arguments or None."""

        if not iscode(co):
            raise TypeError("{!r} is not a code object".format(co))

        nargs = co.co_argcount
        names = co.co_varnames
        nkwargs = co.co_kwonlyargcount
        args = list(names[:nargs])
        kwonlyargs = list(names[nargs : nargs + nkwargs])
        step = 0

        nargs += nkwargs
        varargs = None
        if co.co_flags & CO_VARARGS:
            varargs = co.co_varnames[nargs]
            nargs = nargs + 1
        varkw = None
        if co.co_flags & CO_VARKEYWORDS:
            varkw = co.co_varnames[nargs]
        return args, varargs, kwonlyargs, varkw

    def getfullargspec(func):
        """Get the names and default values of a function's arguments.
    
        A tuple of seven things is returned:
        (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults annotations).
        'args' is a list of the argument names.
        'varargs' and 'varkw' are the names of the * and ** arguments or None.
        'defaults' is an n-tuple of the default values of the last n arguments.
        'kwonlyargs' is a list of keyword-only argument names.
        'kwonlydefaults' is a dictionary mapping names from kwonlyargs to defaults.
        'annotations' is a dictionary mapping argument names to annotations.
    
        The first four items in the tuple correspond to getargspec().
        """

        if ismethod(func):
            func = func.__func__
        if not isfunction(func):
            raise TypeError("{!r} is not a Python function".format(func))
        args, varargs, kwonlyargs, varkw = _getfullargs(func.__code__)
        return FullArgSpec(
            args,
            varargs,
            varkw,
            func.__defaults__,
            kwonlyargs,
            func.__kwdefaults__,
            func.__annotations__,
        )

    def getargs(co):
        """Get information about the arguments accepted by a code object.
    
        Three things are returned: (args, varargs, varkw), where
        'args' is the list of argument names. Keyword-only arguments are
        appended. 'varargs' and 'varkw' are the names of the * and **
        arguments or None."""
        args, varargs, kwonlyargs, varkw = _getfullargs(co)
        return Arguments(args + kwonlyargs, varargs, varkw)

    def getargspec(func):
        """Get the names and default values of a function's arguments.
    
        A tuple of four things is returned: (args, varargs, varkw, defaults).
        'args' is a list of the argument names.
        'args' will include keyword-only argument names.
        'varargs' and 'varkw' are the names of the * and ** arguments or None.
        'defaults' is an n-tuple of the default values of the last n arguments.
    
        Use the getfullargspec() API for Python-3000 code, as annotations
        and keyword arguments are supported. getargspec() will raise ValueError
        if the func has either annotations or keyword arguments.
        """

        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = getfullargspec(
            func
        )
        if kwonlyargs or ann:
            raise ValueError(
                "Function has keyword-only arguments or annotations"
                ", use getfullargspec() API which can support them"
            )
        return ArgSpec(args, varargs, varkw, defaults)


else:
    from inspect import getargspec
    from inspect import getargs
