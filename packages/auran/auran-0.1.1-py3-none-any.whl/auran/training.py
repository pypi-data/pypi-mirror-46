import numpy
from torch.autograd import Variable
import torch.optim as optim
import torch.nn as nn
import torch
from . import recorder
import os
import os.path
import time
import math

class BaseStory(object):
    loss_info_parts = 1
    def __init__(self, trainer, duration, post_roll = 0):
        self.trainer = trainer
        self.start_time = None
        self.duration = duration + post_roll
        self.post_roll = post_roll
        self.loss_info = []

    def finished(self, time):
        if self.start_time == None:
            return False
        return (time - self.start_time) >= self.duration

    def story_init(self):
        """Called at time == 0"""
        self.trainer.reset()

    def story_update(self, story_time):
        raise NotImplementedError()

    def update(self, time):
        assert(not self.finished(time))
        if self.start_time == None:
            self.start_time = time
            self.story_init()

        reltime = time - self.start_time
        if reltime < self.duration - self.post_roll:
            self.story_update(reltime)

    def get_reference(self, story_time):
        # Should return a tensor
        raise NotImplementedError()

    def get_debug_loss(self, story_time):
        return math.sqrt(self.total_loss)

    def post_update(self, time):
        reltime = time - self.start_time

        if reltime < self.duration - self.post_roll:
            self.story_post_update(reltime)

        if reltime < self.duration - self.post_roll - 1:
            self.story_step_finish(reltime)
        elif reltime == self.duration - self.post_roll - 1:
            self.story_finish(reltime)

    def story_post_update(self, story_time):
        self.reference = self.get_reference(story_time)

        # Display

        if not self.trainer.xp.display_disable():
            numpy_reference = self.reference.cpu().data.numpy().flatten()
            numpy_output = self.trainer.network.get_output().cpu().data.numpy().flatten()
            self.trainer.xp.add_display(story_time + self.start_time, "story.reference", numpy_reference)
            self.trainer.xp.add_display(story_time + self.start_time, "story.output", numpy_output)
            if numpy_output.size != numpy_reference.size:
                raise Exception("Output %s and reference %s should have the same size" % (numpy_output.size, numpy_reference.size))
            
            output_and_reference = numpy.stack([numpy_output, numpy_reference], axis = 1)
                
            self.trainer.xp.add_display(story_time + self.start_time, "story.out_and_ref", output_and_reference)
        
        self.total_loss = self.trainer.compute_loss(story_time + self.start_time, self.reference)

        assert(len(self.loss_info) == story_time)

        self.loss_info.append(self.get_debug_loss(story_time))

    def story_step_finish(self, story_time):
        self.trainer.story_step_finish(story_time + self.start_time)

    def story_finish(self, story_time):
        self.trainer.story_finish(story_time + self.start_time)
        self.record_stats(story_time)

    def record_stats(self, story_time):
        pass

    def set_brain_input(self, name, value):
        # TODO : clean this mess
        return self.trainer.xp.organism.brain.set_input(name, value)


class Trainer(object):
    # TODO : override this in subclasses
    story_factory = None
    loss_scaling = 1.0
    loss_aggregate = 1000
    all_step_optimize = False

    def __init__(self, xp, target_steps = 1, post_roll = 0):
        self.xp = xp
        self.criterion = self.criterion_get()
        self.optimizer = None
        self.target_steps = target_steps
        self.post_roll = post_roll
        self.story = None
        self.loss_reset()
        self.loss_history = []
        self.recorder = recorder.Recorder(self.xp)
        self.recorder_init()
        self.recorder.start_new_log_entry()
        self.create_story(0)
        self.story_counter = 0
        self.run_start_time = time.time()

    def recorder_init(self):
        pass

    def create_story(self, timestamp):
        self.story = self.story_factory(self, self.target_steps, self.post_roll)
        self.xp.start_training_sample(timestamp)

    def reset(self):
        self.xp.organism.reset()
        self.network = self.xp.alpha.brain.net

    def loss_reset(self):
        self.loss_info = None

    def loss_fill(self, story):
        loss_info = numpy.array(story.loss_info)

        if self.loss_info is None:
            self.loss_info = numpy.zeros(loss_info.shape, dtype = numpy.float32)

        self.loss_info += loss_info

    def criterion_get(self):
        return nn.MSELoss(reduction='sum')

    def optimizer_init(self, parameters):
        #return optim.Adam(parameters, lr=0.01)
        #return optim.Adadelta(parameters, lr = 0.5)
        #return optim.ASGD(parameters, lr = 0.001)

        #return optim.SGD(parameters, lr=0.00001, momentum=0.5)

        return optim.RMSprop(parameters, lr = 0.0001)

    def optimizer_get(self):
        if self.optimizer == None:
            parameters = filter(lambda p: p.requires_grad, self.network.parameters())
            self.optimizer = self.optimizer_init(parameters)
            self.optimizer.zero_grad()

        return self.optimizer

    def compute_loss(self, time, reference):
        outputs = self.network.get_output()
        ref_outputs = Variable(reference)

        self.loss = self.criterion(outputs, ref_outputs)
        
        return self.loss.data.item()

#    def update_organism(self):
#        # TODO : remove this ??
#        self.xp.organism.update_eye()

    def update(self, t):
        if self.story.finished(t):
            self.story_counter += 1
            if self.story_counter % self.loss_aggregate == 0:
                avg = (self.loss_info / self.loss_aggregate) * self.loss_scaling
                self.loss_history += [avg]
                print("ELAPSED=", time.time() - self.run_start_time , "SPEED =", self.story_counter / (time.time() - self.run_start_time), "\nLOSS after story_count=", self.story_counter, "\n", avg)
                self.loss_reset()
                self.recorder.start_new_log_entry()

            self.xp.add_display(-1, "global.loss", self.loss_history)
            self.recorder.display()

            self.xp.finish_training_sample()

            self.loss_fill(self.story)

            self.create_story(t)

        self.story.update(t)

    def save(self, path):
        if not (self.loss_history is None):
            out = numpy.array(self.loss_history)
            if out.shape != (0,):
                out = out.reshape((out.shape[0], -1))

                indexes = numpy.array([ [i * self.loss_aggregate] for i in range(out.shape[0])])

                out = numpy.append(indexes, out, axis = 1)

                header = "shape = " + str(out.shape)
                loss_file_tmp = os.path.join(path, "loss.txt.tmp")
                loss_file = os.path.join(path, "loss.txt")

                numpy.savetxt(loss_file_tmp, out, header = header)
                os.rename(loss_file_tmp, loss_file)


    def post_update(self, t):
        self.story.post_update(t)

    def optimize(self, t, retain_graph = False):
        optimizer = self.optimizer_get()
        optimizer.zero_grad()

        if self.loss is not None:
            self.loss.backward(retain_graph = retain_graph)
            optimizer.step()


    def story_step_finish(self, t):
        if self.all_step_optimize:
            self.optimize(t, retain_graph = True)
        
        self.network.display(self.xp, t)

    def story_finish(self, t):
        self.optimize(t)
        self.network.display(self.xp, t)
