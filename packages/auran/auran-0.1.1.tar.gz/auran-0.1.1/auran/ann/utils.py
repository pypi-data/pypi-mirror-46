from functools import reduce

def product(elements):
    return reduce(lambda x,y : x * y, elements)

def flat_numpy(tensor):
    return tensor.squeeze().data.numpy()

# Utility class to use python call syntax to create elegant ordered dict
class od(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __iter__(self):
        return iter(self.kwargs.items())
