class UpsampleGen(LayerGen):
    def build(self, input_size):
        layer = nn.Upsample(input_size)
        if layer.size is not None:
            output_size = layer.size
        else:
            output_size = []
            for inp in input_size:
                output_size += [int(inp * layer.scale_factor)]
        output_size = tuple(output_size)

        return layer, output_size
