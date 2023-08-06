import sys

import argspec

py2k = sys.version_info < (3, 0)
py3k = sys.version_info >= (3, 0)
py32 = sys.version_info >= (3, 2)
py38 = sys.version_info >= (3, 8)
py27 = sys.version_info >= (2, 7)


def test(bim, bam=True, boom=1, *args, **kwargs):
    print(bim)
    print(bam)
    print(boom)


if py3k:
    import collections

    ArgSpec = collections.namedtuple(
        "ArgSpec", ["args", "varargs", "keywords", "defaults"]
    )

    if py38:
        from inspect import signature

        def inspect_getargspec(func):
            sig = signature(func)
            args = []
            varargs = None
            varkw = None
            kwonlyargs = []
            defaults = ()
            annotations = {}
            defaults = ()
            kwdefaults = {}
            for param in sig.parameters.values():
                kind = param.kind
                name = param.name

                if kind is param.POSITIONAL_ONLY:
                    args.append(name)
                elif kind is param.POSITIONAL_OR_KEYWORD:
                    args.append(name)
                    if param.default is not param.empty:
                        defaults += (param.default,)
                elif kind is param.VAR_POSITIONAL:
                    varargs = name
                elif kind is param.KEYWORD_ONLY:
                    kwonlyargs.append(name)
                    if param.default is not param.empty:
                        kwdefaults[name] = param.default
                elif kind is param.VAR_KEYWORD:
                    varkw = name

                if param.annotation is not param.empty:
                    annotations[name] = param.annotation

            if not kwdefaults:
                # compatibility with 'func.__kwdefaults__'
                kwdefaults = None

            if not defaults:
                # compatibility with 'func.__defaults__'
                defaults = None

            return ArgSpec(args, varargs, varkw, defaults)

    else:
        from inspect import getfullargspec as inspect_getfullargspec

        def inspect_getargspec(func):
            return ArgSpec(*inspect_getfullargspec(func)[0:4])


else:
    from inspect import getargspec as inspect_getargspec  # noqa


print(inspect_getargspec(test))
