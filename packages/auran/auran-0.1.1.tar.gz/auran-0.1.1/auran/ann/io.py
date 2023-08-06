from . import common, combine, container
from .. import device
import torch.nn as nn

class ReshapeView(nn.Module):
    def __init__(self, shape):
        self.shape = shape
        super(ReshapeView, self).__init__()

    def forward(self, x):
        ret = x.view(1, *self.shape)
        return ret

class ReshapeViewGen(common.LayerGen):
    def __init__(self, shape):
        self.shape = shape

    def build(self, input_size):
        a = 1
        for s in input_size:
            a *= s

        b = 1
        for s in self.shape:
            b *= s

        if a != b:
            raise Exception("ReshapeViewGen: input %s number of elements %s is different from specified shape %s who have %s elements" % (input_size, a, self.shape, b))

        layer = ReshapeView(self.shape)

        return layer, self.shape


class WrapperGen(common.LayerGen):
    def __init__(self, net):
        from .. import brain
        assert(isinstance(net, brain.Net))
        self.net = net

    def build(self, input_size):
#        if input_size != self.net.input_size:
#            raise Exception("Invalid input_size %s : different from wrapped network %s" % (input_size, self.input_size))
        assert(isinstance(self.net.network, container.ContainerLayer))
        return self.net.network, self.net.output_size

class Extract(nn.Module):
    def __init__(self, start, end, *args, **kwargs):
        super(Extract, self).__init__(*args, **kwargs)
        self.start, self.end = start, end
        
    def forward(self, batch):
        return batch[:,self.start:self.end]

class ExtractGen(common.LayerGen):
    def __init__(self, start, end, *args, **kwargs):
        super(ExtractGen, self).__init__(*args, **kwargs)
        self.start, self.end = start, end
        
    def build(self, input_size):
        output_size = list(input_size)
        output_size[0] = self.end - self.start
        layer = Extract(self.start, self.end)
        return layer, tuple(output_size)

    
class TensorHolder(nn.Module):
    def __init__(self, size,  *args, **kwargs):
        super(TensorHolder, self).__init__()
        self.reset([1] + list(size))

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def reset(self, size = None):
        if size is None:
            size = self.value.shape
        self.value = device.zeros(size)

    def forward(self, *args):
        return self.value

class TensorHolderGen(common.LayerGen):
    def __init__(self, size, *args, **kwargs):
        self.size = tuple(size)

    def build(self, input_size):
        layer = TensorHolder(self.size)
        return layer, self.size

class TensorUpdater(nn.Module):
    def __init__(self, name_map, dest_root_name = None, *args, **kwargs):
        # Name map is a list of couples input_name, holder_name
        self.name_map = name_map
        self.dest_root_name = dest_root_name
        assert(self.name_map is not None)

        super(TensorUpdater, self).__init__()

    def forward(self, batch):
        # Get parent for source, and possiblity for destination
        parent = container.get_layer_child_parent(self)
        if self.dest_root_name is not None:
            dest_root = parent.get_module(self.dest_root_name)
        else:
            dest_root = parent

        for src, dest in self.name_map:
            # src name is relative to parent
            src_output = parent.get_output(src)
            # dest name is relative to parent or dest_root if specified
            dest_module = dest_root.get_module(dest)
            old_value = dest_module.get()
            old_value_shape = old_value.shape
            dest_module.set(src_output.view(old_value_shape))
            
        return batch
        
class TensorUpdaterGen(common.LayerGen):
    def __init__(self, name_map, dest_root_name = None, **kwargs):
        # Name map is a list of couples input_name, holder_name
        self.name_map = name_map
        self.dest_root_name = dest_root_name
        super(TensorUpdaterGen, self).__init__()

    def build(self, input_size):
        if self.dest_root_name != None:
            # Get the parent path
            self_name = ".".join(self.full_name().split(".")[1:])
            # Substract the parent path from the dest full path, to get a relative path
            dest_root_name = self.dest_root_name[len(self_name):]
        else:
            dest_root_name = None
        layer = TensorUpdater(self.name_map, dest_root_name)

        return layer, input_size

class RelativeDestTensorUpdaterGen(TensorUpdaterGen):
    def __init__(self, networkWrapper, *args, **kwargs):
        self.networkWrapper = networkWrapper
        # holder_name will be setup in build
        super(RelativeDestTensorUpdaterGen, self).__init__(*args, **kwargs)

    def build(self, input_size):
        self.dest_root_name = self.networkWrapper.full_name()
        return super(RelativeDestTensorUpdaterGen, self).build(input_size)
