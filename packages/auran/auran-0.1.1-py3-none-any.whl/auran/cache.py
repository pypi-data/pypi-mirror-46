import tempfile
import os.path
import functools
import pickle
import inspect
import contextlib


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
           if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects

class disk_cache(object):
    def __init__(self, reset = False):
        self.reset = reset
        
    def __call__(self, func):        
        @functools.wraps(func)
        def memoized_func(*args, **kwargs):
            tmp_dir = tempfile.gettempdir()
            aura_path = os.path.join(tmp_dir, "aura")
            os.makedirs(aura_path, exist_ok = True)

            key = "%s.%s-%s-%s" % (str(get_class_that_defined_method(func).__name__),
                                str(func.__name__),
                                str(args),
                                str(kwargs))
            full_path  = os.path.join(aura_path, key)

#            print("memoized", full_path)
            if not os.path.exists(full_path) or self.reset:
                o = func(*args, **kwargs)
                data = pickle.dumps(o)

                with contextlib.suppress(FileNotFoundError):
                    os.remove(full_path)
                    
                with tempfile.NamedTemporaryFile(dir=os.path.dirname(full_path)) as f:
#                    print("START write %s" % full_path)
                    f.write(data)
                    os.link(f.name, full_path)
#                    print("END write %s", full_path)


            with open(full_path, "rb") as f:
#                print("START load %s" % full_path)
                data = f.read()
                o = pickle.loads(data)
#                print("END load")

            return o

        return memoized_func

    

