import cv2
import numpy

class World(object):
    def __init__(self, xp, resolution):
        super(World, self).__init__()
        self.image = numpy.zeros((resolution[0], resolution[1], 3), numpy.uint8)
        self.root = WorldObject(self, None)
        self.root.parent = self
        self.resolution = resolution
        self.xp = xp

    def size(self):
        return self.resolution

    def center(self):
        return (self.resolution[0] // 2, self.resolution[1] // 2)

    def add_child(self, o):
        self.root.add_child(o)

    def clear(self):
        self.image.fill(0)

    def update(self, timestamp):
        self.clear()
#        print("world draw", timestamp)
        self.root.draw(self.image)
        self.xp.add_display(timestamp, "world", self.image)
        self.root.run(timestamp)
        self.root.debug_draw(self.image)
        self.xp.add_display(timestamp, "world.debug", self.image)

    def get_image(self):
        return self.image

    def save_snapshot(self, file_name):
        cv2.imwrite(file_name, self.image)

    def position(self):
        return numpy.array([0,0])

    def add_display(self, timestamp, name, image):
        self.xp.add_display(timestamp, name, image)

    def get_world_path(self):
        return []

class WorldObject(object):
    def __init__(self, world, translation = None, name = None):
#        super(WorldObject, self).__init__()
        self.world = world
        if translation == None:
            self.translation = numpy.array([0,0])
        else:
            self.translation = numpy.array(translation)
        self.children = []
        self.name = name

    def get_world_path(self):
        return self.parent.get_world_path() + [self.name]

    def add_display(self, timestamp, name, image):
        path = [f for f in self.get_world_path() + [name] if f != None]
        path = ".".join(path)
        self.world.add_display(timestamp, path, image)

    def position(self):
        return self.translation + self.parent.position()

    def add_child(self, c):
        c.parent = self
        self.children += [c]

    def run(self, timestamp):
        for c in self.children:
            c.run(timestamp)

    def draw_self(self, image):
        pass

    def draw(self, image):
        self.draw_self(image)
        for c in self.children:
            c.draw(image)

    def debug_draw_self(self, image):
        pass

    def debug_draw(self, image):
        self.debug_draw_self(image)
        for c in self.children:
            c.debug_draw(image)

class Rect(WorldObject):
    def __init__(self, world, translation, size, color):
        super(Rect, self).__init__(world, translation)
        self.size = size
        self.color = color

    def draw(self, image):
        # Filled rectangle
        pos1 = tuple(self.position())
        pos2 = (pos1[0] + self.size[0], pos1[1] + self.size[1])
        cv2.rectangle(image, pos1, pos2, self.color, -1, cv2.LINE_4)


class Circle(WorldObject):
    def __init__(self, world, translation, radius, color):
        super(Circle, self).__init__(world, translation)
        self.radius = radius
        self.color = color

    def draw(self, image):
        # Filled rectangle
        pos1 = tuple(self.position())
        cv2.circle(image, pos1, self.radius, self.color, -1, cv2.LINE_4)










