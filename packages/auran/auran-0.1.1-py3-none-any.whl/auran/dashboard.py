import collections
import numpy
import matplotlib.ticker
import matplotlib.pyplot as pyplot
import math
import _thread
import time


class Figure(object):
    def __init__(self, config, image_name, image, *args, **kwargs):
        self.config = config
        self.name = image_name
        self.image = image
        if not isinstance(self.image, numpy.ndarray):
            self.image = numpy.array(self.image)
        self.args = args
        self.kwargs = kwargs
        self.size = numpy.array(image).shape

    def run(self):
        self.plot_call(self.image, *args, **kwargs)

    def draw(self, sp):
        #                sp.set_xticks([i for i in range(figure.image.shape[0])])
#                sp.set_yticks([i for i in range(figure.image.shape[0])]

        sp.tick_params(axis='both', which='major', labelsize=4, length=2, pad=1, reset = False)

        sp.set_title(self.name, size=10)

class ImageFigure(Figure):
    def draw(self, sp):
        super(ImageFigure, self).draw(sp)
        scale = 1

        for shape_axis in self.image.shape:
            while shape_axis > scale * 10:
                scale *= 10

        majorLocator = matplotlib.ticker.MultipleLocator(scale)
        minorLocator = matplotlib.ticker.MultipleLocator(1)

        sp.xaxis.set_major_locator(majorLocator)
#        sp.xaxis.set_minor_locator(minorLocator)
        sp.yaxis.set_major_locator(majorLocator)
#        sp.yaxis.set_minor_locator(minorLocator)

        pyplot.imshow(self.image, interpolation = "none")

class PlotFigure(Figure):
    def draw(self, sp):
        super(PlotFigure, self).draw(sp)
        non_one = 0
        for s in self.size:
            if s != 1:
                non_one += 1

        legend = []
        image = self.image

        transpose = self.config.transpose
        if transpose != None and transpose != False:
            if transpose is True:
                transpose = [1, 0]
            image = numpy.transpose(image, transpose)

        if non_one <= 1:
            image = image.flatten()
            legend += [self.config.legend_prefix]
        else:
            for i in range(self.size[1]):
                legend += [self.config.legend_prefix + str(i)]

        if self.config.legend != None:
            legend = self.config.legend

        pyplot.plot(image)

        if len(legend) > 1:
            sp.legend(legend, loc='upper left')

class ColorBarFigure(Figure):
    def draw(self, sp):
        try:
            pyplot.colorbar(cax=sp, orientation = "vertical")
        except Exception as e :
            print(e)

        frame_index = 10
        pyplot.text(0.0, -0.15, "frame=%d" % frame_index, fontsize=12)

class Config(object):
    figure_factory = None
    # Is the object bound to a story time ? (True, except for LossPlotConfig that does not depend on specific story time)
    frame_based = True

    def image_names(self, image_name):
        return [image_name]

    def new_figures_from_image(self, image_name, image):
        ret = []
        for image_name, image in self.process_image(image_name, image):
            ret += [self.figure_factory(self, image_name, image)]
        return ret

    def process_image(self, image_name, image):
        return [(image_name, image)]

class PlotConfig(Config):
    figure_factory = PlotFigure

    def __init__(self, legend = None, legend_prefix = "graph", transpose = None):
        super(PlotConfig, self).__init__()
        self.legend_prefix = legend_prefix
        self.transpose = transpose
        self.legend = legend

class LossPlotConfig(PlotConfig):
    figure_factory = PlotFigure
    frame_based = False

    def image_names(self, image_name):
        return [(image_name + "#" + sn) for sn in self.sub_names]

    def __init__(self, sub_names = ["loss"], legend_prefix = "loss"):
        super(LossPlotConfig, self).__init__()
        self.legend_prefix = legend_prefix
        self.sub_names = sub_names
        self.transpose = None

    def process_image(self, image_name, image):
        initial_loss_image = numpy.array(image)
        initial_name = image_name

        loss_images = []
        if len(initial_loss_image.shape) == 3:
            last_dim_size = initial_loss_image.shape[2]
            if last_dim_size > len(self.sub_names):
                raise Exception("Not enough names in LossPlotConfig : loss last dimension is %d, and sub_names are %s" % (last_dim_size, self.sub_names))
            for i in range(last_dim_size):
                subimage_name = initial_name  + "#" + self.sub_names[i]
                subimage = initial_loss_image[:,:,i]
                loss_images += [(subimage_name, subimage)]
        else:
            if len(initial_loss_image.shape) == 1 and initial_loss_image.shape[0] != 0:
                assert(len(self.sub_names) == 1)

            return [(image_name + "#" + sn, initial_loss_image) for sn in self.sub_names]

        return loss_images

class ColorBarConfig(Config):
    figure_factory = ColorBarFigure
    frame_based = False

class ImageConfig(Config):
    figure_factory = ImageFigure

class DefaultImageConfig(ImageConfig):
    pass

class RGBImageConfig(ImageConfig):
    def process_image(self, image_name, image):
        image = numpy.transpose(image[0], (1, 2, 0))
        return [(image_name, image)]

class FlattenImageConfig(ImageConfig):
    def __init__(self, transpose = False, *args, **kwargs):
        self.transpose = transpose
        super(FlattenImageConfig, self).__init__(*args, **kwargs)

    def process_image(self, image_name, image):
        shape = image.shape
        if len(shape) == 4:
            if shape[3] == 1 :
                new_shape = [shape[0] * shape[1], shape[2]]
            else:
                new_shape = [shape[0] * shape[1] * shape[2], shape[3]]
        if len(shape) == 3:
            new_shape = [shape[0] * shape[1], shape[2]]
        elif len(shape) == 2:
            new_shape = shape
        elif len(shape) == 1:
            new_shape = [shape[0], 1]

        image = image.reshape(new_shape)

        if self.transpose:
            image = image.transpose()
        
        return [(image_name, image)]

class SquareImageConfig(ImageConfig):
    def __init__(self, divider, parts = None, transpose = False):
        self.divider = divider
        self.parts = parts or [1]
        self.transpose = transpose

    def image_name_build(self, image_name, index):
        return image_name + "@%d" % index

    def image_names(self, image_name):
        ret = []
        for i in range(len(self.parts)):
            ret += [self.image_name_build(image_name, i)]
        return ret

    def process_image(self, image_name, image):
        # input should be displayed as a square, with info[1] channels
        divider = self.divider
        parts = self.parts

        if len(image.shape) == 4:
            s = image.shape
            image = image.reshape([s[0] * s[1], s[2] * s[3]])
        if self.transpose:
            image = image.transpose()
#        print("process_image", image_name, image.shape)
        size0 = image.shape[1]

        size0 //= sum(parts)

        start = 0
        images = []
        for part_index, p in enumerate(parts):
            size = size0 * p
            size = int(math.sqrt(size))
            amount = size * size
            stop  = start + amount
            img = image[:,start:start + amount]
            start = stop
            img = img.reshape([divider * size, size])
            images += [(self.image_name_build(image_name, part_index), img)]
        if (stop != image.shape[1]):
            if not(hasattr(self, "debug_first")):
                print("STOPPING BEFORE IMAGE END", stop, image.shape, image_name)
        return images

def pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
    while b != 0:
        r=a%b
        a,b=b,r
    return a

def ppcm(a,b):
    """ppcm(a,b): calcul du 'Plus Petit Commun Multiple' entre 2 nombres entiers a et b"""
    if (a==0) or (b==0):
        return 0
    else:
        return (a*b)//pgcd(a,b)

class DashboardLayoutConfig(object):
    def __init__(self):
        self.whitelist = {}
        self.rows = collections.OrderedDict()
        self.rows_config = collections.OrderedDict()

    def add_display(self, row_name, name, config):
        if row_name not in self.rows:
            self.rows[row_name] = collections.OrderedDict()

        for n in config.image_names(name):
            self.rows[row_name][n] = config

        self.whitelist[name] = row_name

    def set_row_config(self, row_name, key, value):
        if row_name not in self.rows_config:
            self.rows_config[row_name] = {}
        self.rows_config[row_name][key] = value

    def get_row_config(self, row_name, key, default):
        return self.rows_config.get(row_name, {}).get(key, default)

    def get(self, name):
        row_name = self.whitelist.get(name)
        if row_name is None:
            return None

        ret = self.rows.get(row_name).get(name, None)
        if ret:
            return ret

        # Try subnames, as some images generate several figures, return the first one
        for figure_name, config in self.rows.get(row_name).items():
            if figure_name.startswith(name):
                return config

    def ppcm_cols(self):
        m = 1
        for name, c in self.rows.items():
            m = ppcm(m, len(c))
        return m

    def rows_total_size(self):
        total_size = 0
        for name, c in self.rows.items():
            total_size += self.get_row_config(name, "width", 1)
        return total_size

class DashboardFrame(object):
    def __init__(self, frame_index):
        self.frame_index = frame_index
        self.figures = {}

    def add_figure(self, figure):
        self.figures[figure.name] = figure

    def get_figure(self, name):
        return self.figures.get(name, None)

class DashboardFrameSet(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.frames = []
        self.append(DashboardFrame(0))

    def append(self, frame):
        self.frames.append(frame)

    def add_display(self, timestamp, figure):
        if timestamp == -1:
            frame_index = 0
        else:
            frame_index = timestamp - self.timestamp

        while len(self.frames) <= frame_index:
            self.append(DashboardFrame(len(self.frames)))

        self.frames[frame_index].add_figure(figure)

    def get_frame_count(self):
        return len(self.frames)

    def get_frame(self, frame_index):
        return self.frames[frame_index]

    def get_figure_count(self):
        fcount = 0
        for f in self.frames:
            fcount = max(fcount, len(f.get_figures()))
        return fcount

class Dashboard(object):
    def __init__(self, config, backend):
        self.config = config
        self.backend = backend
        self.debug = False
        self.started = False
        self.started_timestamp = None

    def start_sequence(self, timestamp):
        if not self.started:
            self.new_frame_set = DashboardFrameSet(timestamp)
            self.started = True
            self.started_timestamp = timestamp

    def accept_display(self, timestamp):
        return self.started

    def display_figure_enabled(self, name):
        dashboard_config = self.config.get("dashboard/layout")
        if dashboard_config == None:
            return None
        return dashboard_config.get(name)

    def add_display(self, timestamp, image_name, image):
        if not self.started:
            return

        image = image.copy()
        figure_config = self.display_figure_enabled(image_name)
        if self.debug:
            print(image_name, figure_config)
        if figure_config is not None:
            figures = figure_config.new_figures_from_image(image_name, image)
            for figure in figures:
                if self.debug:
                    print(figure.name, timestamp)

                self.new_frame_set.add_display(timestamp, figure)

    def end_sequence(self):
        if not self.started:
            return

        frame_set = self.new_frame_set
        self.new_frame_set = None

        dashboard_config = self.config.get("dashboard/layout")
        self.backend.display(frame_set, dashboard_config)

        self.started = False

    def display_refresh(self, filename = None, frame_index = None):
        self.backend.display_refresh(filename, frame_index = frame_index)

class DashboardBackend(object):
    def display(self, frame_set):
         # To be implemented by subclasses
        pass

class MPLBackend(DashboardBackend):
    def __init__(self, config):
        self.mp_fig = None
        self.config = config
        self.last_time = 0.0
        self.frame_index = 0
        self.frame_set = None
        self.first = True

    def display(self, frame_set, dashboard_config):
        self.frame_set = frame_set
        self.dashboard_config = dashboard_config

        self.frame_index = 0
        self.display_refresh()

    def display_refresh(self, filename = None, frame_index = None):
        if self.frame_set == None:
            return

        if frame_index == None:
            t = time.time()
            if (t - self.last_time) < self.config.get("dashboard/story_refresh", 1.0):
                return
            self.last_time = t

            if self.frame_index >= self.frame_set.get_frame_count():
                self.frame_index = 0
                # Pause a bit : we should not return, but it creates a single frame pause
                return
            use_frame_index = self.frame_index
        else:
            use_frame_index = frame_index

        self.display_init(self.dashboard_config)

        self.display_core(self.frame_set, self.dashboard_config, use_frame_index)
        #        self.mp_fig.tight_layout()
        self.display_finish(self.dashboard_config, filename)

        if frame_index == None:
            self.frame_index += 1


    def display_init(self, dashboard_config):
        if self.mp_fig == None:
            figsize = self.config.get("dashboard/size", (12, 6))
            self.mp_fig = pyplot.figure(num=self.config.get("xp/name"), figsize=figsize)

        pyplot.clf()

    def display_core(self, frame_set, dashboard_config, frame_index):
        ppcm_cols = dashboard_config.ppcm_cols()
        rows_total_size = dashboard_config.rows_total_size()

        row_offset = 0
        sps = []
        for row_index, (row_name, row) in enumerate(dashboard_config.rows.items()):
            rowspan = dashboard_config.get_row_config(row_name, "height", 1)
            colspan = ppcm_cols // len(row.items())

            for col_index, (figure_name, figure_config) in enumerate(row.items()):
                sp = pyplot.subplot2grid((rows_total_size, ppcm_cols), (row_offset, col_index * colspan),
                                         rowspan=rowspan, colspan=colspan)
                sps += [sp]
                if figure_config.frame_based:
                    figure_frame_index = frame_index
                else:
                    figure_frame_index = 0
                figure = frame_set.get_frame(figure_frame_index).get_figure(figure_name)
                if figure is None:
                    valid_names = ",".join(frame_set.get_frame(figure_frame_index).figures.keys())
                    print("Invalid figure name %s, figure_frame_index = %d, valid names are: %s" % (figure_name, figure_frame_index, valid_names))
                    continue

                figure.draw(sp)
                try:
                    pyplot.colorbar()
                except:
                    pass

            row_offset += rowspan

    def pause(self, interval):
        # From https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7/45734500#45734500
        backend = pyplot.rcParams['backend']
        if backend in matplotlib.rcsetup.interactive_bk:
            figManager = matplotlib._pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                canvas.start_event_loop(interval)
                return
            
    def display_finish(self, dashboard_config, filename):
        margin = 0.05
        pyplot.subplots_adjust(left=margin, right=1.0-margin, top=1.0 - margin, bottom=margin, hspace = 0.2, wspace = 0.4)

        if self.first:
            pyplot.show(block=False)
            self.first = False

        if filename != None:
            self.pause(0.5)
            self.display_save(filename)
        else:
            self.pause(0.00000001)

    def display_save(self, filename):
        pyplot.savefig(filename)




