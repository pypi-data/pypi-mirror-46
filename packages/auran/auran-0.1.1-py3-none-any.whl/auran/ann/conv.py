from . import common
import torch.nn as nn
import copy
import math

class ConvLikeBaseGen(common.LayerGen):
    def computeSize(self, layer, Hin, Win, kernel_size, padding, stride, dilation):
        Hout = (Hin + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) // stride[0] + 1
        Wout = (Win + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) // stride[1] + 1

        return Hout, Wout

    def kernel_size_helper(self, kernel_size, input_size, dilation = None):
        out_kernel_size = []
        for i in range(len(kernel_size)):
            if kernel_size[i] == -1:
                ks = input_size[i + 1]
                if dilation != None:
                    ks = int(math.ceil(ks / dilation[i]))

                out_kernel_size += [ks]
            else:
                out_kernel_size += [kernel_size[i]]
        out_kernel_size = tuple(out_kernel_size)
        return out_kernel_size

class ConvLikeGen(ConvLikeBaseGen):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, *args, **kwargs):
        super(ConvLikeGen, self).__init__(*args, **kwargs)
        if isinstance(kernel_size, int):
            kernel_size = [kernel_size, kernel_size]
        if isinstance(dilation, int):
            dilation = [dilation, dilation]
        self.conv_kwargs = {"in_channels" : in_channels,
                            "out_channels" : out_channels,
                            "kernel_size" : kernel_size,
                            "stride" : stride,
                            "padding": padding,
                            "dilation" : dilation,
                            "groups" : groups,
                            "bias" : bias}

class Conv2dGen(ConvLikeGen):
    def build(self, input_size):
        self.conv_kwargs["kernel_size"] = self.kernel_size_helper(self.conv_kwargs["kernel_size"], input_size, self.conv_kwargs["dilation"])
        layer = nn.Conv2d(*self.args, **self.conv_kwargs)
        ret = self.build_helper(layer, input_size)
#        print(input_size, layer, ret[0], ret[1])
        return ret

class ConvTranspose2dGen(ConvLikeGen):
    def set_linked_conv(self, conv):
        self.__linked_conv__ = conv

    def computeSize(self, layer, Hin, Win, kernel_size, padding, stride, dilation):
        Hout = (Hin - 1) * stride[0] - 2 * padding[0] + kernel_size[0] + layer.output_padding[0]
        Wout = (Win - 1) * stride[1] - 2 * padding[1] + kernel_size[1] + layer.output_padding[1]
        return Hout, Wout

    def build(self, input_size):
        if hasattr(self, "__linked_conv__"):
            self.conv_kwargs["kernel_size"] = self.__linked_conv__.conv_kwargs["kernel_size"]
        self.conv_kwargs["kernel_size"] = self.kernel_size_helper(self.conv_kwargs["kernel_size"], input_size, self.conv_kwargs["dilation"])
        layer = nn.ConvTranspose2d(*self.args, **self.conv_kwargs)
        return self.build_helper(layer, input_size)

class ConvTransposeHelper(object):
    def __init__(self, conv_array, decoder_input_channels):
        self.conv_array = conv_array
        self.decoder_input_channels = decoder_input_channels

    def run(self):
        out_array = []

        for i, c in enumerate(self.conv_array):
            if isinstance(c, tuple):
                name = c[0]
                c = c[1]
            else:
                name = None
            if (isinstance(c, Conv2dGen)):
                last_conv_index = i

        for i, c in enumerate(self.conv_array):
            if isinstance(c, tuple):
                name = c[0]
                c = c[1]
            else:
                name = None

            if (isinstance(c, Conv2dGen)):
                kwargs = copy.deepcopy(c.conv_kwargs)
                kwargs["out_channels"] = c.conv_kwargs["in_channels"]
                if i != last_conv_index:
                    in_channels = c.conv_kwargs["out_channels"]
                else:
                    in_channels = self.decoder_input_channels
                kwargs["in_channels"] = in_channels
#                print(i, last_conv_index, in_channels, kwargs)

                ct = ConvTranspose2dGen(**kwargs)
                ct.set_linked_conv(c)
                insert_index = 0
            else:
                insert_index = 1
                ct = copy.deepcopy(c)

            if name != None:
                ct = (name + "_tr", ct)

            out_array.insert(insert_index, ct)

        return out_array
