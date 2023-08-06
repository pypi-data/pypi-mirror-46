import torch.nn as nn
from . import common

class BatchNorm2dGen(common.LayerGen):
    def build(self, input_size):
        layer = nn.BatchNorm2d(input_size[0])
        return layer, input_size


class BatchNorm1dGen(common.LayerGen):
    def build(self, input_size):
        layer = nn.BatchNorm1d(input_size[0])
        return layer, input_size
