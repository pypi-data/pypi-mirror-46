import torch
import torch.nn as nn
from . import conv
from .. import device

class MaxPool2dGen(conv.ConvLikeBaseGen):
    # If kernel size has -1 somewhere, it means we should collapse the given dimension
    def __init__(self, kernel_size = None, target_size = None, *args, **kwargs):
        super(MaxPool2dGen, self).__init__(*args, **kwargs)
        self.kernel_size = kernel_size
        self.target_size = target_size

    def build(self, input_size):
        if self.target_size != None:
            self.kernel_size = [s // self.target_size for s in input_size]        

        kernel_size = self.kernel_size_helper(self.kernel_size, input_size)
        layer = nn.MaxPool2d(kernel_size, *self.args, **self.kwargs)

        return self.build_helper(layer, input_size)


class AvgPool2dGen(conv.ConvLikeBaseGen):
    # If kernel size has -1 somewhere, it means we should collapse the given dimension
    def __init__(self, kernel_size = None, *args, target_size = None, **kwargs):
        super(AvgPool2dGen, self).__init__(*args, **kwargs)
        self.kernel_size = kernel_size
        self.target_size = target_size

    def compute_size(self, layer, Hin, Win, kernel_size, padding, stride, dilation):
        Hout = (Hin + 2 * padding[0] - kernel_size[0]) // stride[0] + 1
        Wout = (Win + 2 * padding[1] - kernel_size[1]) // stride[1] + 1
        return Hout, Wout

    def build(self, input_size):
        if self.target_size != None:
            self.kernel_size = [s // self.target_size for s in input_size]
                    
        kernel_size = self.kernel_size_helper(self.kernel_size, input_size)
        layer = nn.AvgPool2d(kernel_size, *self.args, **self.kwargs)

        ret = self.build_helper(layer, input_size)
        return ret

class WinnerTakeAll2D(nn.Module):
    def __init__(self, input_size, avg_kernel_size, *args, **kwargs):
        super(WinnerTakeAll2D, self).__init__(*args, **kwargs)
        self.input_size = input_size
        self.avg_kernel_size = avg_kernel_size
            
        self.max_pool_kernel_size = (input_size[1] // avg_kernel_size[0], input_size[2] // avg_kernel_size[1])
#        print(self.max_pool_kernel_size, input_size, avg_kernel_size)
        
        self.avg_pool = nn.AvgPool2d(kernel_size = self.avg_kernel_size)
        self.max_pool = nn.MaxPool2d(kernel_size = self.max_pool_kernel_size, return_indices = True)
        self.xy_grid = None

    def forward(self, batch):
        output = self.avg_pool(batch)
        maxoutput, maxpos = self.max_pool(torch.abs(output))
        index = maxpos.item()
        
        if self.xy_grid is None:
            x_size = batch.shape[2]
            y_size = batch.shape[3]
            x_cord = torch.arange(x_size)
            x_grid = x_cord.repeat(y_size).view((x_size, y_size))
            y_cord = torch.arange(y_size)
            y_grid = y_cord.repeat(x_size).view((y_size, x_size)).t()
            
            self.xy_grid = torch.stack([x_grid, y_grid], dim=-1).type(torch.FloatTensor)

        if batch.shape[2] != batch.shape[3]:
            assert(False) # This case was not tested, x_index,y_index and variance may have to be changed
            
        x_index = (index % output.shape[2]) * self.avg_kernel_size[0]
        y_index = (index // output.shape[2]) * self.avg_kernel_size[1]

        std_dev = float(batch.shape[2] / self.avg_kernel_size[0]) / 3.0

        mean = device.tensor([x_index, y_index])
        gaussian = -torch.sum((self.xy_grid - mean)**float(2.0), dim=-1)
        gaussian /= (std_dev ** 2) * 2.0
        gaussian = torch.exp(gaussian)
#        gaussian /= torch.sum(gaussian)

        gaussian = gaussian.unsqueeze(0).unsqueeze(0)
        return gaussian
        
class WinnerTakeAll2DGen(conv.ConvLikeBaseGen):
    def __init__(self, target_size = None, kernel_size = None, *args, **kwargs):
        super(WinnerTakeAll2DGen, self).__init__(*args, **kwargs)
        self.kernel_size = kernel_size
        self.target_size = target_size
    
    def build(self, input_size):
        if self.target_size != None:
            if isinstance(self.target_size, int):
                self.target_size = [self.target_size] * 2
            self.kernel_size = []
            for i, s in enumerate(input_size[1:]):
                self.kernel_size += [s // self.target_size[i]]
                    
        kernel_size = self.kernel_size_helper(self.kernel_size, input_size)

        for i, s in enumerate(input_size[1:]):
            if s % kernel_size[i] != 0:
                raise Exception("The input size %s is not a multiple of kernel_size %s" % (input_size, kernel_size))                
        
        net = WinnerTakeAll2D(input_size, avg_kernel_size = (4,4))

#        output_size = (input_size[0], input_size[1] // kernel_size[0], input_size[2] // kernel_size[1])
#        print(input_size, output_size)

        return net, input_size
