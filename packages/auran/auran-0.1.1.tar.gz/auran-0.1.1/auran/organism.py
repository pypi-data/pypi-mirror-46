from . import world, cache, ann
import numpy
import cv2
import math

class Organ(world.WorldObject):
    def __init__(self, world, translation, name):
        super(Organ, self).__init__(world, translation, name)


# Old defaults
#    eye_reach = 32
#    retina_scale_down = 2
#    retina_final_scale_down = 2
#    scale_mode = 0
#    centered_eye = False
#    noise_level = 0.03


class EyeConfig(object):
    def __init__(self, reach = 0.5, retina_scale_down = 1, retina_final_scale_down = 16, scale_mode = 2, centered = False, noise_level = 0.03):
        self.reach = reach
        self.retina_scale_down = retina_scale_down
        self.retina_final_scale_down = retina_final_scale_down
        self.scale_mode = scale_mode
        self.centered = centered
        self.noise_level = noise_level
        

class Eye(Organ):
    def __init__(self, world, translation, config):               
        super(Eye, self).__init__(world, translation, "eye")
        self.color = (128, 128, 255)

        # Base resolution is world size
        self.input_resolution = world.size()
        self.scale_mode = config.scale_mode
        self.noise_level = config.noise_level
        if config.centered:
            multiplier = 1
        else:
            multiplier = 2
        self.tmp_retina_resolution = [multiplier * self.input_resolution[0], multiplier * self.input_resolution[1]]
        assert(self.tmp_retina_resolution[0] % 2 == 0)
        assert(self.tmp_retina_resolution[1] % 2 == 0)

        # Scale in two phases : first while doing retina fovea remapping, second simple scaling down with averaging of pixels
        self.retina_scale_down = config.retina_scale_down
        self.retina_final_scale_down = config.retina_final_scale_down
        # Temporary retina
        self.tmp_retina = numpy.zeros((self.tmp_retina_resolution[0], self.tmp_retina_resolution[1], 3), numpy.float)

        resolution = numpy.array(self.tmp_retina_resolution, numpy.int)
        resolution //= self.retina_scale_down * self.retina_final_scale_down
        self.resolution = (3, resolution[0], resolution[1])

        # Build the static remapping used for fovea
        self.build_remap()
        self.confidence_radius = None
        
    def set_output_result(self, o, function_name, function_args):
        self.output_result_callback = [o, function_name, function_args]

    def call_output_result(self, image):
        info = self.output_result_callback
        fun = getattr(info[0], info[1])
        fun(image, *info[2])
        
    def clear(self):
        """Clear the image where the world is pasted into (with translation)"""
        self.tmp_retina.fill(0)

    @staticmethod
    @cache.disk_cache(reset = False)
    def build_remap_impl(shape, scale_mode, retina_scale_down):
        center = numpy.array(shape) / 2.0
        retina_mapx = numpy.zeros(shape, numpy.float32)
        retina_mapy = numpy.zeros(shape, numpy.float32)
        scale = math.pow(shape[0] / 2.0, - scale_mode) * math.pow(retina_scale_down, scale_mode + 1)
        for i in range(shape[0]):
            for j in range(shape[1]):
                pos = numpy.array([i, j], numpy.float)
                pos -= center
                pos *= scale * math.pow(cv2.norm(pos), scale_mode)
                pos += center
                retina_mapy[i,j] = pos[0]
                retina_mapx[i,j] = pos[1]
        return retina_mapx, retina_mapy
        
    def build_remap(self):
        """Build the cv2.remap map"""
        shape = (self.tmp_retina.shape[0], self.tmp_retina.shape[1])


        self.retina_mapx, self.retina_mapy = self.build_remap_impl(shape, self.scale_mode, self.retina_scale_down)

    def run(self, timestamp):
        """Run the eye acquisition, putting the result in self.retina"""
        self.clear()
        image = self.world.get_image()

        image = numpy.array(image, numpy.float) / 255.0

        #Crop the world image into self.tmp_retina
        position = self.position()
        left = max(0, position[0] - self.tmp_retina.shape[0] // 2)
        top = max(0, position[1] - self.tmp_retina.shape[1] // 2)
        right = min(image.shape[0], position[0] + self.tmp_retina.shape[0] // 2)
        bottom = min(image.shape[1], position[1] + self.tmp_retina.shape[1] // 2)

        crop = image[top:bottom, left:right]

        xpos = left - (position[0]  - self.tmp_retina.shape[0] // 2)
        ypos = top - (position[1]  - self.tmp_retina.shape[1] // 2)

        self.tmp_retina[ypos:ypos + bottom - top, xpos:xpos + right - left] = crop

        # Remap self.tmp_retina into a new image
        pre_retina = cv2.remap(self.tmp_retina, self.retina_mapx, self.retina_mapy, interpolation = cv2.INTER_AREA)

        # Crop the center of the retina
        shape = pre_retina.shape

        r = self.retina_scale_down
        if r != 1:
            e = shape[0] // r // 2
            rmin = (r - 1) * e
            rmax = (r + 1) * e
            pre_retina = pre_retina[rmin:rmax, rmin:rmax]

        # Resize the retina to its final size
        if self.retina_final_scale_down == 1:
            self.retina = pre_retina
        else:
            final_scale = 1.0 / self.retina_final_scale_down
            self.retina = cv2.resize(pre_retina, None, fx = final_scale, fy = final_scale, interpolation = cv2.INTER_AREA)

        self.retina = numpy.array(self.retina, numpy.float)
        r = numpy.random.random_sample(self.retina.shape) * self.noise_level
        self.retina += r
        self.retina *= (1.0/ (1.0 + self.noise_level))

        self.add_display(timestamp, "retina", self.retina)

        image = numpy.transpose(self.retina, (2, 0, 1))
        shape = image.shape
        image = image.reshape([-1, shape[0], shape[1], shape[2]])
        image = numpy.array(image, dtype=numpy.float32)

        self.call_output_result(image)

    def debug_draw_self(self, image):
        pos = tuple(self.position())
#        print("debug_draw_self", pos)
        pos1 = (pos[0] - 2, pos[1] - 2)
        pos2 = (pos[0] + 2, pos[1] + 2)
        cv2.rectangle(image, pos1, pos2, self.color, -1, cv2.LINE_4)
        if self.confidence_radius != None:
            cv2.circle(image, pos, int(self.confidence_radius), (0,255,0))

    def draw_self(self, image):
        pos = tuple(self.position())
        pos1 = (pos[0] - 2, pos[1] - 2)
        pos2 = (pos[0] + 2, pos[1] + 2)
#        cv2.rectangle(image, pos1, pos2, (255, 0, 255), -1, cv2.LINE_4)

class Hand(Organ):
    def __init__(self, world, translation):
        self.color = (0,255,255)
        super(Hand, self).__init__(world, translation, "hand")

    def debug_draw_self(self, image):
        pos = tuple(self.position())
        pos1 = (pos[0] - 3, pos[1] - 3)
        pos2 = (pos[0] + 3 , pos[1] + 3)
        cv2.rectangle(image, pos1, pos2, self.color, -1, cv2.LINE_4)


class Organism(world.WorldObject):
    def __init__(self, world, translation):
        super(Organism, self).__init__(world, translation, "org")

class DummyBrain(Organ):
    def __init__(self, world, organism):
        super(DummyBrain, self).__init__(world, None)
        self.organism = organism
        self.hand_position = numpy.array([0.0,0.0])
        self.eye_position = numpy.array([0.0,0.0])

    def run(self, timestamp):
        random = numpy.random.random(size=(2,)) * 0.05 - 0.025
        self.hand_position += random
        random = numpy.random.random(size=(2,)) * 0.02 - 0.01
        self.eye_position += random

    def get_output(self, name):
        if name == "hand":
            return self.hand_position
        elif name == "eye":
            return self.eye_position        

class HandConfig(object):
    def __init__(self, reach = 0.5):
        self.reach = reach
    
class Alpha(Organism):
    has_hand = True
    has_eye = True
    
    def __init__(self, world, translation = None, configs = {}, *args, **kwargs):        
        world_size = world.resolution
        if translation is None:
            translation = list(numpy.array(world.resolution) // 2)
            
        super(Alpha, self).__init__(world, translation)
        self.configs = configs
        
        if self.has_hand:
            hand_config = self.configs.get("hand", HandConfig())
            self.hand_reach = self.build_reach(world_size, hand_config.reach)

            self.hand = Hand(world, None)            
            self.add_child(self.hand)
                
        if self.has_eye:
            eye_config = self.configs.get("eye", EyeConfig())
            self.eye_reach = self.build_reach(world_size, eye_config.reach)
        
            self.eye = Eye(world, None, eye_config)
            self.eye.set_output_result(self, "set_brain_input", ["image"])        
            self.add_child(self.eye)
            

    def build_reach(self, world_size, reach):
        return int(world_size[0] * reach)

    def set_brain_input(self, data, name):
        # Data should be a numpy image
        self.brain.set_input(name, data)
        
    def save(self, path):
        print("Saving to", path)
        self.brain.save(path)

    def set_brain(self, brain):
        self.brain = brain
        self.add_child(self.brain)

    def normalize_output(self, value, scale, bounds):
        t = numpy.multiply(value, scale)
        t = numpy.ndarray.astype(t, numpy.int)
        t = numpy.minimum(t, bounds)
        t = numpy.maximum(t, - bounds)
        return t

    def reset(self):
#        print("organism reset")
        if self.has_hand:
            self.hand.translation = numpy.array([0,0])
        if self.has_eye:
            self.eye.translation = numpy.array([0,0])
        self.brain.reset()

    def run(self, timestamp):
        super(Alpha, self).run(timestamp)
        if self.has_eye:
            hand = self.brain.get_output("hand")
            self.hand.translation = self.normalize_output(hand, self.hand_reach, self.hand_reach)

        if self.has_eye:
            eye = self.brain.get_output("eye")
            self.eye.translation = self.normalize_output(eye, self.eye_reach, self.eye_reach)

        eye_confidence = self.brain.get_output("eye_confidence")
        if eye_confidence is not None:
            self.eye.confidence_radius = eye_confidence * self.eye_reach[0]

    def create_brain(self):
        return DummyBrain(world, self)





