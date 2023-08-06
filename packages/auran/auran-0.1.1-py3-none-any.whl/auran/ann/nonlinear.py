from . import common
import torch
import torch.nn as nn
import torchgeometry.contrib
from .. import device

class ReLUGen(common.LayerGen):
    Layer = nn.ReLU

class LeakyReLUGen(common.LayerGen):
    Layer = nn.LeakyReLU

class SigmoidGen(common.LayerGen):
    Layer = nn.Sigmoid

class TanhGen(common.LayerGen):
    Layer = nn.Tanh

class LogSigmoidGen(common.LayerGen):
    Layer = nn.LogSigmoid

class SoftplusGen(common.LayerGen):
    Layer = nn.Softplus

class Square(nn.Module):
    def forward(self, batch):
        return torch.mul(batch, batch)

class SquareGen(common.LayerGen):
    Layer = Square
    
class Abs(nn.Module):
    def forward(self, batch):
        return torch.abs(batch)
    
class AbsGen(common.LayerGen):
    Layer = Abs
    
class Exp(nn.Module):
    def forward(self, batch):
        return torch.exp(batch)

class ExpGen(common.LayerGen):
    Layer = Exp

class Gauss(nn.Module):
    def forward(self, batch):
        return torch.exp(-batch * batch)

class GaussGen(common.LayerGen):
    Layer = Gauss
    
class LogSoftmaxGen(common.LayerGen):
    Layer = nn.LogSoftmax
    
class SoftmaxGen(common.LayerGen):
    Layer = nn.Softmax
    
class Softmax2dGen(common.LayerGen):
    Layer = nn.Softmax2d

class SoftmaxSurface(nn.Module):
    def __init__(self, mode = None, *args, **kwargs):
        self.mode = mode
        super(SoftmaxSurface, self).__init__(*args, **kwargs)
        
    def forward(self, batch):
        shape = [s for s in batch.shape]
        if self.mode == "exp2":
            shape[1] *= 2
            
        ret = device.zeros(shape)
        for i in range(batch.shape[0]):
            for j in range(batch.shape[1]):
                e = batch[i][j]
                
                if self.mode in ["exp2", "exp2"]:
                    e = torch.exp(e - torch.max(e))
                    s = torch.sum(e)
                    
                    if s.item() != 0:
                        if self.mode == "exp2":
                            ret[i][2 * j] = e / s
                        else:
                            ret[i][j] += e / 2.0

                    e = torch.exp(- e + torch.min(e))
                    s = torch.sum(e)
                    
                    if s.item() != 0:
                        if self.mode == "exp2":                            
                            ret[i][2 * j + 1] = e / s
                        else:
                            ret[i][j] += e / (s * 2.0)
                elif self.mode in ["square"]:
                    m = torch.mean(e)
                    e = (e - m) ** 2
                    s = torch.sum(e)
                    
                    if s.item() != 0:
                        ret[i][j] = e / s
                        
                else:
                    s = torch.sum(torch.abs(e))
                    
                    if s.item() != 0:
                        ret[i][j] = e / s               
        return ret

class SoftmaxSurfaceGen(common.LayerGen):
    def __init__(self, mode = None, *args, **kwargs):
        self.mode = mode
        super(SoftmaxSurfaceGen, self).__init__(*args, **kwargs)
        
    def build(self, input_size):
        layer = SoftmaxSurface(self.mode, *self.args, **self.kwargs)

        output_size = [s for s in input_size]
        if self.mode == "exp2":
            output_size[0] *= 2
            return layer, output_size
        else:
            return layer, output_size

    
class SpatialSoftArgmax2dGen(common.LayerGen):
    def build(self, input_size, *args, **kwargs):
        layer = torchgeometry.contrib.SpatialSoftArgmax2d(*args, **kwargs)
        return layer, (2,)



