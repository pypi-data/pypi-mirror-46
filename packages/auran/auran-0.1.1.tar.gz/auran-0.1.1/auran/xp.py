import os
import sys
import time
import datetime
import numpy
from . import world, dashboard, config
from matplotlib import pyplot
import os.path
import traceback

class Experiment(object):
    # TODO : override this in subclasses
    trainer_factory = None

    @staticmethod
    def aura_xp_data_path():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "aura_xp_data"))

    def __init__(self, size = 320, base_path = None, config_path = None):
        self.world = world.World(self, (size,size))
        self.debug_images = {}
        self.windows = {}
        self.current_offset = [00, 0]
        if base_path == None:
            base_path = self.aura_xp_data_path()
        self.base_path = base_path

        # load config from config_path, or if it is None, from experiment python file itself, calling fill_config function
        self.config = config.Config(config_path or sys.modules[self.__module__].__file__)
        self.config.set("xp/name", self.get_xp_name())
        self.dashboard = dashboard.Dashboard(self.config, dashboard.MPLBackend(self.config))

        self.dashboard_last_update_time = 0.0

    def create_world(self):
        pass

    def create_organism(self):
        pass

    def update(self, time):
        self.trainer.update(time)

    def post_update(self, time):
        self.trainer.post_update(time)

    def display_disable(self):
        return self.config.get("dashboard/display_disable", False)

    def accept_display(self, timestamp):
        ret = self.dashboard.accept_display(timestamp)
        return ret
    
    def start_training_sample(self, timestamp):
        """Used to signal we are starting a new training sample"""
        try:
            self.config.reload()
        except Exception as e:
            traceback.print_exc()
        max_elapsed = self.config.get("dashboard/refresh", 1.0)

        t = time.time()
        elapsed = t - self.dashboard_last_update_time

        if self.display_disable():
            return
        
        if elapsed >= max_elapsed:
            self.dashboard_last_update_time = t
            self.dashboard.start_sequence(timestamp)
        else:
            self.dashboard.display_refresh()

    def finish_training_sample(self):
        self.dashboard.end_sequence()

    def add_display(self, timestamp, image_name, image):
        try:
            self.dashboard.add_display(timestamp, image_name, image)
        except Exception as e:
            print("Could not display %s" % image_name)
            traceback.print_exc()

    def get_xp_name(self):
        import sys
        f = os.path.split(sys.modules[self.__module__].__file__)[-1]
        xp_name = os.path.splitext(f)[0]
        return xp_name

    def get_xp_module(self):
         # TEMPORARY
        return "fl_ml.aura.xps." + self.get_xp_name()

    def get_latest_path(self):
        return self.get_latest_path_for_name(self.get_xp_name())

    @staticmethod
    def get_latest_path_for_name(xp_name):
        input_dir = os.path.abspath(os.path.join(Experiment.aura_xp_data_path(), "xps", xp_name))

        # Get the last subdirectories (the dir names all finish by a date)
        dates = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
        dates = [d for d in dates if os.path.isdir(d)]
        dates.sort(reverse = True)

        max_dir = None

        for last in dates:
            max_epoch = -1
            for g in os.listdir(last):
                if not os.path.isdir(os.path.join(last, g)):
                    continue
                epoch = -1
                try:
                    epoch = int(g.split("_")[1])
                except Exception as e:
                    print("Could not parse %s : %s" % (g, e))
                if epoch > max_epoch:
                    max_dir = os.path.join(last, g)
                    max_epoch = epoch
            if max_dir != None:
                return max_dir
            else:
                print("The directory did not contain a valid network, maybe was interrupted early: %s" % last)

    def run(self, max_time):
        print("----------- STARTING -----------")
        directory = [self.get_xp_name()]
        directory += [str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")]

        full_path = os.path.abspath(os.path.join(self.base_path, "xps", *directory))
        self.save_path = full_path
        print("SAVE PATH IS", self.save_path)

        for obj in self.create_world():
            if obj != None:
                self.world.add_child(obj)

        self.organism = self.create_organism()
        self.world.add_child(self.organism)

        self.trainer = self.trainer_factory(self)

        for i in range(0, max_time, 1):
            self.update(i)
            self.world.update(i)
            self.post_update(i)

            if (i % self.config.get("network_save_epochs", 10000)) == 0 or i == (max_time - 1):
                full_path0 = os.path.join(self.save_path, "epoch_" + str(i))
                os.makedirs(full_path0)
                self.organism.save(full_path0)
                self.trainer.save(self.save_path)

                full_path_screenshot = os.path.join(full_path0, "screenshot.png")
                self.dashboard.display_refresh(full_path_screenshot, self.trainer.target_steps - 1)

        pyplot.close()

        print("----------- FINISHED -----------")

        # Return last save path
        return full_path0


