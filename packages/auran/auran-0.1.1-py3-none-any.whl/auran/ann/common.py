class LayerGen(object):
    def __init__(self, *args, **kwargs):
        super(LayerGen, self).__init__()
        self.args = args
        if "post_hook" in kwargs:
            self.post_hook = kwargs["post_hook"]
            del kwargs["post_hook"]
        else:
            self.post_hook = None
        self.kwargs = kwargs

    def build(self, input_size):
        layer = self.Layer(*self.args, **self.kwargs)
        return layer, input_size

    def get_input_names(self):
        return None

    def full_name(self):
        if hasattr(self, "parent"):
            name = self.parent.find_child_name(self)
            parent_name = self.parent.full_name()
            if parent_name is not None:                
                return parent_name + "." + name
            else:
                return name
        else:
            return None

    def build_helper(self, layer, input_size):
#        print ("build_helper", input_size)
        Hin = input_size[1]
        Win = input_size[2]
        Cin = input_size[0]
        if not hasattr(layer, "out_channels"):
            Cout = Cin
        else:
            Cout = layer.out_channels

        if hasattr(layer, "dilation"):
            dilation = layer.dilation
        else:
            dilation = 0
        if isinstance(dilation, int):
            dilation = (dilation, dilation)

        padding = layer.padding
        if isinstance(padding, int):
            padding = (padding, padding)

        stride = layer.stride
        if isinstance(stride, int):
            stride = (stride, stride)

        Hout, Wout = self.computeSize(layer, Hin, Win, layer.kernel_size, padding, stride, dilation)
        output_size = (Cout, Hout, Wout)

        # TODO : move this to the right place
        if self.post_hook:
            self.post_hook(layer, output_size)

        return layer, output_size

    def compute_size(self, layer, Hin, Win, kernel_size, padding, stride, dilation):
        raise NotImplementedError("%s should implement compute size" % self.__class__.__name__ )
