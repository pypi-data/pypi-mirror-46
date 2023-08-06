import torch
import torch.nn as nn
import torch.distributions as distributions
from . import common
from .. import device


class Sampler(nn.Module):
    def __init__(self, backflow = False, mean_scale = 1.0, stddev_scale = 1.0, distrib_type = "normal"):
        self.backflow = backflow
        self.mean_scale = device.tensor([mean_scale])
        self.stddev_scale = device.tensor([stddev_scale])
        if distrib_type not in ["normal", "uniform"]:
            raise Exception("Unknown distribution type %s, should be normal or uniform" % self.distrib_type)

        self.distrib_type = distrib_type
        super(Sampler, self).__init__()
        
    def forward(self, batch):
        size = batch.shape[1] // 2

        if self.distrib_type == "normal":
            distrib = distributions.Normal(batch[:,::2] * self.mean_scale, torch.abs(batch[:,1::2]) * self.stddev_scale)
        elif self.distrib_type == "uniform":
            center = batch[:,::2] * self.mean_scale
            half_size = torch.abs(batch[:,1::2]) * self.stddev_scale * 0.5

            low = center - half_size
            high = center + half_size
            
            distrib = distributions.Uniform(low, high)
            
        if self.backflow:
            return distrib.rsample()
        else:
            return distrib.sample()
    
class SamplerGen(common.LayerGen):
    def __init__(self, backflow = False, mean_scale = 1.0, stddev_scale = 1.0, distrib_type = "normal"):
        self.mean_scale = mean_scale
        self.stddev_scale = stddev_scale
        self.backflow = backflow
        self.distrib_type = distrib_type
        if distrib_type not in ["normal", "uniform"]:
            raise Exception("Unknown distribution type %s, should be normal or uniform" % self.distrib_type)

        super(SamplerGen, self).__init__()
        
    def build(self, input_size):
        layer = Sampler(self.backflow, self.mean_scale, self.stddev_scale, self.distrib_type)
        return layer, (input_size[0] // 2,)

class GaussianDistribution(nn.Module):
    def __init__(self, gaussian_parameters, *args, **kwargs):
        super(GaussianDistribution, self).__init__(*args, **kwargs)
        self.gaussian_parameters = (torch.Tensor(gaussian_parameters[0]), torch.Tensor(gaussian_parameters[1]))
        
    def forward(self, batch):
        ret = distributions.Normal(*self.gaussian_parameters).sample()
        return ret
    
class GaussianDistributionGen(common.LayerGen):
    def __init__(self, gaussian_parameters, *args, **kwargs):
        self.gaussian_parameters = gaussian_parameters
        super(GaussianDistributionGen, self).__init__(*args, **kwargs)
        
    def build(self, input_size):
        layer = GaussianDistribution(self.gaussian_parameters)
        assert(len(self.gaussian_parameters[0]) == len(self.gaussian_parameters[1]))
        return layer, (len(self.gaussian_parameters[0]),)


class UniformDistribution(nn.Module):
    def __init__(self, uniform_parameters, *args, **kwargs):
        super(UniformDistribution, self).__init__(*args, **kwargs)
        self.uniform_parameters = (torch.Tensor(uniform_parameters[0]), torch.Tensor(uniform_parameters[1]))
        
    def forward(self, batch):
        ret = distributions.Uniform(*self.uniform_parameters).sample()
        return ret
    
class UniformDistributionGen(common.LayerGen):
    def __init__(self, uniform_parameters, *args, **kwargs):
        self.uniform_parameters = uniform_parameters
        super(UniformDistributionGen, self).__init__(*args, **kwargs)
        
    def build(self, input_size):
        layer = UniformDistribution(self.uniform_parameters)
        assert(len(self.uniform_parameters[0]) == len(self.uniform_parameters[1]))
        return layer, (len(self.uniform_parameters[0]),)    
