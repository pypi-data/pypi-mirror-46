import os
from . import xp, brain
import shutil

class Cryo(object):
    def __init__(self, path = None):
        """path is the place where all the best networks are saved"""
        if path == None:
            path = os.path.join(xp.Experiment.aura_xp_data_path(), "cryo")

        self.path = os.path.abspath(path)

    def load_network(self, name, *args, **kwargs):
        path = os.path.join(self.path, name)
        return brain.Net.network_create_and_load(path, *args, **kwargs)

    def save_last_network(self, xp_name, name, force = False):
        src = xp.Experiment.get_latest_path_for_name(xp_name)

        try:
            print("date/hour     : %s" % os.path.split(os.path.split(src)[0])[-1])
            print("max_epoch (k) : %d" % (int(os.path.split(src)[-1].split("_")[-1]) // 1000))
        except:
            pass

        dest = os.path.join(self.path, name)
        if os.path.exists(dest) and force:
            shutil.rmtree(dest)

        shutil.copytree(src, dest)
        shutil.copy(os.path.join(src, "../loss.txt"), os.path.join(dest, "loss.txt"))

class Utils(object):
    @staticmethod
    def inspect(filename, path_to_layer, layer_component):
        assert(path_to_layer.startswith("net."))
        path_to_layer = path_to_layer[4:]
        net = brain.Net.network_create_and_load(filename)
        layer = net.network.get_module(path_to_layer)
        component = getattr(layer, layer_component)

        print(component)



