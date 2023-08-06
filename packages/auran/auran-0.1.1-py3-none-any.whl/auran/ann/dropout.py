from . import common
import torch.nn as nn

class DropoutGen(common.LayerGen):
    def build(self, input_size):
        layer = nn.Dropout(*self.args, **self.kwargs)
        return layer, input_size
