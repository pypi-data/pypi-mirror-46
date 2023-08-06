import torch
import torch.nn as nn
from . import common, conv, utils
from .. import device


class MultiInputModule(nn.Module):
    def __init__(self, input_names, *args, **kwargs):
        self.input_names = input_names
        super(MultiInputModule, self).__init__(*args, **kwargs)

    def get_input_names(self):
        return self.input_names


class MultiInputModuleGen(common.LayerGen):
    def __init__(self, input_names, *args, **kwargs):
        if not isinstance(input_names, list) and not isinstance(input_names, tuple):
            input_names = [input_names] + list(args)
            args = []
        self.input_names = input_names
        super(MultiInputModuleGen, self).__init__(*args, **kwargs)

    def get_input_names(self):
        return self.input_names

class Get(MultiInputModule):
    def __init__(self, input_names, *args, **kwargs):
        super(Get, self).__init__(input_names, *args, **kwargs)
        
    def forward(self, *args):
        ret = args[0]
        return ret
    
class GetGen(MultiInputModuleGen):
    def __init__(self, input_name, *args, **kwargs):
        super(GetGen, self).__init__([input_name], *args, **kwargs)
        
    def build(self, input_sizes):
        layer = Get(self.input_names, *self.args, **self.kwargs)
        size = input_sizes[0]
            
        return layer, size

class Concat(MultiInputModule):
    def forward(self, *args):
        inputs = []
        for y in args:
            inputs += [y.view(1, -1)]

        if len(inputs) == 1:
            output = inputs[0]
        else:
            output = torch.cat(inputs, 1)
        return output
    
class ConcatGen(MultiInputModuleGen):
    def input_size_flatten(self, input_size):
        i = 1
        for j in input_size:
            i *= j
        return i

    def build(self, input_sizes):
        layer = Concat(self.input_names, *self.args, **self.kwargs)

        size = 0
        for input_size in input_sizes:
            size += self.input_size_flatten(input_size)

        return layer, (size,)

class TwoWayConv2d(MultiInputModule):
    def __init__(self, input_names, conv_layer):
        super(TwoWayConv2d, self).__init__(input_names)
        self.conv_layer = conv_layer
        
    def forward(self, *args):
        c = self.conv_layer
        shape = c.weight.shape
        weight = args[1].reshape(shape)
        
        return torch.nn.functional.conv2d(args[0], weight, bias = None, stride=c.stride, padding=c.padding, dilation=c.dilation, groups=c.groups)
            
class TwoWayConv2dGen(MultiInputModuleGen, conv.ConvLikeGen):
    def __init__(self, input_names, *args, **kwargs):
        self.input_names = input_names
        conv.ConvLikeGen.__init__(self, *args, **kwargs)
        
    def build(self, input_sizes):
        self.conv_kwargs["kernel_size"] = self.kernel_size_helper(self.conv_kwargs["kernel_size"], input_sizes[0], self.conv_kwargs["dilation"])

        conv_layer = nn.Conv2d(*self.args, **self.conv_kwargs)
        conv_layer, output_size = self.build_helper(conv_layer, input_sizes[0])
        
        layer = TwoWayConv2d(self.input_names, conv_layer)
        
        return layer, output_size            


class MaskedOperation(MultiInputModule):
    def __init__(self, input_names, masks = None, *args, **kwargs):
        if masks is not None:
            assert(len(masks) == len(input_names))            
            self.masks = [device.tensor(m) for m in masks]
        else:
            self.masks = None
        super(MaskedOperation, self).__init__(input_names, *args, **kwargs)

class MaskedOperationGen(MultiInputModuleGen):
    def __init__(self, input_names, masks = None, *args, **kwargs):
        if masks is not None:
            assert(len(masks) == len(input_names))
            self.masks = [device.tensor(m) for m in masks]
        else:
            self.masks = None
        super(MaskedOperationGen, self).__init__(input_names, *args, **kwargs)
    
class Add(MaskedOperation):
    def forward(self, *args):        
        output = args[0]
        if self.masks is not None:
            output = output.mul(self.masks[0])
            
        for i, y in enumerate(args[1:]):
            if self.masks is not None:
                y = y.mul(self.masks[1 + i])

            output = output.add(y)

        return output

class AddGen(MaskedOperationGen):
    def build(self, input_sizes):
        layer = Add(self.input_names, self.masks, *self.args, **self.kwargs)

        input_size0 = tuple(input_sizes[0])

        for input_size in input_sizes[1:]:
            if(input_size0 != tuple(input_size)):
                print("AddGen incorrect input sizes !!", input_size0, input_size)
            assert(input_size0 == tuple(input_size))

        return layer, input_size0

class Mul(MultiInputModule):
    def forward(self, *args):
        output = args[0]
        for i, y in enumerate(args[1:]):
            output = output.mul(y)

        return output

class MulGen(MultiInputModuleGen):
    def build(self, input_sizes):
        layer = Mul(self.input_names, *self.args, **self.kwargs)

        input_size0 = tuple(input_sizes[0])

        for input_size in input_sizes[1:]:
            if(input_size0 != tuple(input_size)):
                print("MulGen incorrect input sizes !!", input_size0, input_size)
            assert(input_size0 == tuple(input_size))

        return layer, input_size0

    

class Cross(MultiInputModule):
    def forward(self, *args):
        shape0 = args[0].shape
        shape1 = args[1].shape

        s0 = (shape0[0], utils.product(shape0[1:]), 1)
        s1 = (shape1[0], 1, utils.product(shape1[1:]))

        args0 = args[0].reshape(s0)
        args1 = args[1].reshape(s1)
        output = args0 * args1

        output = output.reshape(shape0[0], s0[1] * s1[2])
        
        return output

class CrossGen(MultiInputModuleGen):
    def build(self, input_sizes):
        assert(len(input_sizes) == 2)
        layer = Cross(self.input_names, *self.args, **self.kwargs)

        m = 1
        for input_size in input_sizes:
            m *= utils.product(input_size)

        return layer, (m,)
