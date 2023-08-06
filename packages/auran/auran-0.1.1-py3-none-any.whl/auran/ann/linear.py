from . import common
from .. import device
import torch
import torch
import torch.nn as nn
import torch.nn.parameter as parameter
import random
        
class Scale(nn.Module):
    def __init__(self, scale, *args, **kwargs):
        super(Scale, self).__init__(*args, **kwargs)
        self.scale = scale
        
    def forward(self, batch):
        return batch * self.scale
    
class ScaleGen(common.LayerGen):
    def __init__(self, scale, *args, **kwargs):
        super(ScaleGen, self).__init__(*args, **kwargs)
        self.scale = scale
        
    def build(self, input_size):
        if input_size[0] != len(self.scale):
            raise Exception("Invalid length %s for scale parameter : should be %s." % (len(self.scale), input_size[0]))
        layer = Scale(device.prepare_object(device.tensor(self.scale)))
        return layer, input_size

class LogCascade(nn.Module):
    def __init__(self, precision, output_dimensions, *args, **kwargs):
        super(LogCascade, self).__init__(*args, **kwargs)
        self.precision = precision
        self.output_dimensions = output_dimensions
        self.weights = []
        w = 0.5
        for i in range(self.precision):
            self.weights += [w]
            w /= 2
        self.weights = device.prepare_object(device.tensor(self.weights))
        
    def forward(self, batch):
        batch = batch.reshape([-1, self.output_dimensions, self.precision])
        output = torch.matmul(batch, self.weights)
        
        return output
    
class LogCascadeGen(common.LayerGen):
    def __init__(self, output_dimensions, *args, **kwargs):
        super(LogCascadeGen, self).__init__(*args, **kwargs)
        self.output_dimensions = output_dimensions
        
    def build(self, input_size):
        p = product(input_size)
        if p % self.output_dimensions != 0:
            raise Exception("Invalid input size %s, product of input sizes must be a multiple of output_dimensions %s" % (p, self.output_dimensions))
        layer = LogCascade(p / output_dimensions, output_dimensions)
        return layer, input_size


class LinearBaseGen(common.LayerGen):
    def __init__(self, out_features, *args, **kwargs):
        self.out_features = out_features
        super(LinearBaseGen, self).__init__(*args, **kwargs)

    def build(self, input_size):
        in_features = input_size[-1]

        layer = self.Constructor(in_features, self.out_features, *self.args, **self.kwargs)

        output_size = tuple(input_size[:-1]) + (self.out_features,)

        if self.post_hook != None:
            self.post_hook(layer, output_size)

        return layer, output_size

class LinearGen(LinearBaseGen):
    Constructor = nn.Linear

class LinView(nn.Module):
    def __init__(self, truncate = 1):
        self.truncate = truncate
        super(LinView, self).__init__()

    def forward(self, x):
        size = x.size()
        t = [size[0]]

        for i in range(1, len(size) - self.truncate - 1):
            t += [size[i]]
        t += [-1]
        ret = x.view(*t)

        return ret

class LinViewGen(common.LayerGen):
    def __init__(self, truncate = 1):
        self.truncate = truncate

    def build(self, input_size):
        layer = LinView(self.truncate)
        size = input_size

        t = []
        for i in range(0, len(size) - self.truncate - 1):
            t += [size[i]]

        m = 1
        for i in range(max(0, len(size) - self.truncate - 1), len(size)):
            m *= size[i]

        t += [m]

        output_size = tuple(t)
        return layer, output_size


class OpParam(nn.Module):
    def __init__(self, size, collapse, distribute = True, normal_mean_init = 0.0, normal_std_init = 1.0, *args, **kwargs):
        super(OpParam, self).__init__()
        self.weight = nn.Parameter(torch.FloatTensor(size))
        # Is this the right way to initialize weights ?
        torch.nn.init.normal(self.weight, mean = normal_mean_init, std=normal_std_init)
        self.collapse = collapse
        self.distribute = distribute
        self.args = args
        self.kwargs = kwargs

    def forward(self, batch):
        weights_count = self.weight.shape[0]
        if self.collapse:
            batch_repeat = [1] * len(batch.shape)
            if self.distribute:
                batch_repeat[-1] *= weights_count
                weights_repeat = [s for s in batch.shape]
            else:
                assert(weights_count % batch.shape[-1] == 0)
                batch_repeat[-1] *= weights_count // batch.shape[-1]
                weights_repeat = [s for s in batch.shape]
                weights_repeat[-1] = 1
        else:
            batch_repeat = [1] * len(batch.shape) + [weights_count]
            if self.distribute:
                weights_repeat = [s for s in batch.shape] + [1]
            else:
                # TODO
                assert(False)
                weights_repeat = [s for s in batch.shape] + [1]

#        print(batch_repeat, batch.shape)
#        print(weights_repeat, self.weight.shape)
        batch = batch.repeat(*batch_repeat)
        weights = self.weight.repeat(*weights_repeat)
        
        return self.op(batch, weights)

    
class OpParamGen(common.LayerGen):
    def __init__(self, size, collapse = False, distribute = True, *args, **kwargs):
        self.size = size
        self.distribute = distribute
        self.collapse = collapse
        super(OpParamGen, self).__init__(*args, **kwargs)
        
    def build(self, input_size):
        layer = self.OpParam(self.size, self.collapse, self.distribute, *self.args, **self.kwargs)
        output_size = [s for s in input_size]
        if self.distribute:
            if self.collapse:        
                output_size[-1] *= self.size
            else:
                output_size += [self.size]
        else:
            output_size[-1] = self.size
        output_size = tuple(output_size)
        return layer, output_size


class AddParam(OpParam):
    def op(self, batch, weights):
        return batch + weights

class SubParam(OpParam):
    def op(self, batch, weights):
        return batch - weights
    
class MulParam(OpParam):
    def op(self, batch, weights):
        sign = self.kwargs.get("sign", 0)
        if sign== 1:
            weights = abs(weights)
        elif sign == -1:
            weights = -abs(weights)
            
        ret = batch * weights
        return ret

class SubParamGen(OpParamGen):
    OpParam = SubParam

class AddParamGen(OpParamGen):
    OpParam = AddParam
  
class MulParamGen(OpParamGen):
    OpParam = MulParam

class Neg(nn.Module):
    def forward(self, batch):
        return - batch

class Neg(common.LayerGen):
    Layer = Neg


class SparseLinear(nn.Module):
    def __init__(self, in_features, out_features = None, weight = True, bias = True, *args, **kwargs):
        super(SparseLinear, self).__init__()

        if not weight:
            assert(out_features == None)
            out_features = in_features

        self.in_features = in_features
        self.out_features = out_features
        
        if weight:
            self.weight = parameter.Parameter(self.create_weight(*args, **kwargs))
        else:
            self.register_parameter('weight', None)
            
        if bias:
            self.bias = parameter.Parameter(self.create_bias())
        else:
            self.register_parameter('bias', None)

    def create_bias(self):
        return device.zeros(self.out_features)        
            
    def create_sparse_weight_default(self, max_x, max_y, bands = 1, overlap = 0):
        # The caller guarantees that max_x < max_y
        assert(max_x <= max_y)
        ratio = (max_y / max_x) / bands

        x = []
        y = []
        for b in range(bands):
            for i in range(max_x):
                start = i * ratio
                end = (i + 1) * ratio

                for j in range(round(start - overlap / 2.0), round(end + overlap / 2.0)):
                    if j <= 0:
                        j += max_y

                    RAND = 4
                    # Wrap around, it's important so the first and last lines have two neighbours, and not just one
                    y_index = ((b * max_y) / bands + j + max_y + random.randint(-RAND, RAND)) % max_y 

                    x_index = i
                    
                    x += [x_index]
                    y += [y_index]

        return x, y 
                                
    def create_sparse_weight(self, *args, **kwargs):
        max_x = self.out_features
        max_y = self.in_features

        transpose = False
        if max_x > max_y:
            max_x, max_y = max_y, max_x
            transpose = True

        x, y = self.create_sparse_weight_default(max_x, max_y, *args, **kwargs)

        if transpose:
            return y, x
        else:
            return x, y
                              
        
    def create_weight(self, normal_mean_init = 0.0, normal_std_init = 1.0, *args, **kwargs):
        x, y = self.create_sparse_weight(*args, **kwargs)
        
        self.indexes = [x,y]
        self.values = torch.zeros(len(self.indexes[0]))

        # Is this the right way to initialize weight ?
        torch.nn.init.normal(self.values, mean = normal_mean_init, std=normal_std_init)

        self.values = torch.abs(self.values)

        self.indexes = torch.LongTensor(self.indexes)
        
        ret = torch.sparse.FloatTensor(torch.LongTensor(self.indexes),
                                       self.values,
                                       torch.Size([self.out_features, self.in_features]))

        ret = ret.coalesce()
        return ret
    
    def forward(self, input):
        if self.weight is not None:
            b = input[0].reshape(input[0].shape[0], -1)
            output = torch.sparse.mm(self.weight, b)
            output = output.reshape(output.shape[0])            
            
        if self.bias is not None:
            output += self.bias
            
        return output.reshape(1, -1)
        
class SparseLinearGen(LinearBaseGen):
    Constructor = SparseLinear
