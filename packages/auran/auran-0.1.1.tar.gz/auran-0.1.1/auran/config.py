import importlib.util
import os.path

"""Config keys:
  dashboard.update_freq : frequency in hz, default 1hz
"""

class Config(object):
    def __init__(self, config_path):
        """config_path is the path to a python file with a "fill_config" method that will be called to fill this object.
This allows some code to generate the config, and to reload it periodically after the user has changed it.
         """
        self.config_path = config_path
        self.config_path_time_stamp = None
        self.info = {}
        if config_path != None:
            self.reload()

    def regularize(self, path):
        if not isinstance(path, list):
            path = path.split("/")
        return path

    def get(self, path, default = None):
        path = self.regularize(path)
        d = self.info
        for p in path[:-1]:
            d = d.get(p, {})

        return d.get(path[-1], default)

    def set(self, path, value):
        path = self.regularize(path)
        d = self.info
        for i, p in enumerate(path[:-1]):
            if p not in d:
                d[p] = {}
            d = d[p]

        d[path[-1]] = value


    def dump(self, root = None):
        if root == None:
            root = self.info

        for k, v in self.info.items():
            if isinstance(v, dict):
                self.dump(v)
            else:
                print("%s -> %s" % (k,v))


    def reload(self):
        mtime = os.path.getmtime(self.config_path)
        if mtime == self.config_path_time_stamp:
#            print("No change")
            return
        self.config_path_time_stamp = mtime

        # Reload the module. From https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        spec = importlib.util.spec_from_file_location("__aura_config__", self.config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call the function fill_config on the module
        self.info = {}
        new_config = Config(None)
        module.fill_config(new_config)
        self.info = new_config.info
#        self.dump()
