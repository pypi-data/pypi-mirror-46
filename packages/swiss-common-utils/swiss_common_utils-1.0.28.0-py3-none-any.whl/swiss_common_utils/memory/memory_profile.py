from memory_profiler import profile


def record_memory_usage(activate=False, stream=None):
    def wrap(org_func):
        if activate:

            @profile(stream=stream)
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)

            return wrapped_func
        else:
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)

            return wrapped_func

    return wrap
