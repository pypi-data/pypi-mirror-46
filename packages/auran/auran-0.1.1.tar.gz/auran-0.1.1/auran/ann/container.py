import collections
from . import common, io, combine
import torch.nn as nn
    
CHILD_PARENT = {}

def get_layer_child_parent(child):
    return CHILD_PARENT[id(child)]

def set_layer_child_parent(child, parent):
    CHILD_PARENT[id(child)] = parent
    
class ContainerLayer(object):
    def get_module_and_output(self, output_name):
        output_name_split = output_name.split(".")
        
        child_name = output_name_split[0]

        if len(child_name) == 0:
            return get_layer_child_parent(self).get_module_and_output(".".join(output_name_split[1:]))
        
        if child_name not in self._modules:
            knowns = ", ".join(self._modules.keys())
            raise Exception("Unknown name %s in object %s, know names are %s" % (child_name, self.__class__.__name__ , knowns))
        m = self._modules[child_name]

        if len(output_name_split) == 1:
            outputs = None
            if hasattr(self, "outputs"):
                outputs = self.outputs[output_name]
            return m, outputs
        else:
            return m.get_module_and_output(".".join(output_name_split[1:]))

    def set_output(self, output_name, batch):
        self.outputs[output_name] = batch

    def get_output(self, output_name = None):
        if output_name == None:
            return self.outputs[output_name]
        return self.get_module_and_output(output_name)[1]

    def get_module(self, output_name):
        return self.get_module_and_output(output_name)[0]

    def display(self, xp, timestamp, current_path = []):
        if xp.display_disable() or not xp.accept_display(timestamp):
            return
        for child_name, child in self._modules.items():
            if isinstance(child, ContainerLayer):
                child.display(xp, timestamp, current_path + [child_name])
                continue

            module_full_name = ".".join(current_path + [child_name])
            output = self.get_output(child_name)
            image = output.cpu().data.clone().numpy()

            xp.add_display(timestamp, "net." + module_full_name + "#out", image)

            if hasattr(child, "weight") and child.weight is not None:
                weight = child.weight
                if weight.is_sparse:
                    weight = weight.to_dense()
                image = weight.cpu().data.clone().numpy()
                xp.add_display(timestamp, "net." + module_full_name + "#w", image)

            if hasattr(child, "bias") and child.bias is not None:
                image = child.bias.data.clone().numpy()
                xp.add_display(timestamp, "net." + module_full_name + "#b", image)




class ContainerLayerGen(common.LayerGen):
    def __init__(self, *args, **kwargs):
        super(ContainerLayerGen, self).__init__(*args, **kwargs)
        self.child_and_output_sizes = {}
        self.prepared = False
        self.parent_assigned = False
        
    def build(self, *args, **kwargs):
#        print("build", self.__class__.__name__, id(self), self.prepared)
        if not self.prepared:
            self.prepare()
            self.prepared = True
        return self.build_(*args, **kwargs)

    def prepare(self):
        self.assign_parent()

    def enumerate_python_args(self):
        return enumerate(self.args)
        
    def enumerate_children(self):
        for i, c in self.enumerate_python_args():
            if isinstance(c, tuple):
                name = c[0]
                obj = c[1]
            else:
                name = "#%d" % i
                obj = c
            yield name, obj

    def find_child_name(self, child):
        for name, c in self.enumerate_children():
            if c == child:
                return name

    def assign_parent(self):
        if self.parent_assigned:
            return
        self.parent_assigned = True

        for name, obj in self.enumerate_children():
#            print("assign_parent", self.__class__.__name__, id(self), obj.__class__.__name__, id(obj))
            obj.parent = self
            if hasattr(obj, "assign_parent"):
                obj.assign_parent()

    def get_output_size(self, name):
        name_split = name.split(".")

        if len(name_split[0]) == 0:
            return self.parent.get_output_size(".".join(name_split[1:]))

        if name_split[0] not in self.child_and_output_sizes:
            raise Exception("Could not find %s in %s: name set is %s" % (name_split[0], self, [ k for k in self.child_and_output_sizes.keys()]))
                            
        child, output_size = self.child_and_output_sizes[name_split[0]]
        if len(name_split) == 1:
            return output_size
        else:
            return child.get_output_size(".".join(name_split[1:]))

    def add_child_and_output_size(self, name, child, output_size):
        self.child_and_output_sizes[name] = (child, output_size)


class Broadcast(nn.Module, ContainerLayer):
    def __init__(self, children, *args, **kwargs):
        super(Broadcast, self).__init__(*args, **kwargs)
        for c in children:
            self.add_module(c[0], c[1])

    def forward(self, *args):
        self.outputs = {}
        outputs = []
        for n in self._modules.items():
            module_name = n[0]
            module = n[1]
            output = module(*args)
            self.set_output(module_name, output)
            outputs += [output]

        return outputs[0]

class BroadcastGen(ContainerLayerGen):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.child_enumerator_object = kwargs
            # kwargs is used to list child names
            kwargs = {}
        else:
            self.child_enumerator_object = args
            
        super(BroadcastGen, self).__init__(*args, **kwargs)

    def enumerate_python_args(self):
        if isinstance(self.child_enumerator_object, dict):
            return enumerate(self.child_enumerator_object.items())
        else:
            assert(isinstance(self.child_enumerator_object, list) or isinstance(self.child_enumerator_object, tuple))
            return enumerate(self.child_enumerator_object)
    
    def input_size_flatten(self, input_size):
        i = 1
        for j in input_size:
            i *= j
        return i

    def build_(self, input_size = None):
        modules = []
        first_final_size = None
        
        for name, obj in self.enumerate_children():
            module, final_size = obj.build(input_size)
            if first_final_size == None:
                first_final_size = final_size

            self.add_child_and_output_size(name, obj, final_size)

            modules += [(name, module)]

        layer = Broadcast(modules, **self.kwargs)

        for name, m in modules:
            set_layer_child_parent(m, layer)

        return layer, first_final_size

class Sequential(nn.Sequential, ContainerLayer):
    def forward(self, *args):
        self.outputs = {}

        batch = None
        for index, n in enumerate(self._modules.items()):
            module_name = n[0]
            module = n[1]

            if isinstance(module, combine.MultiInputModule):
#                print('Multi input')
                input_names = module.get_input_names()
                inputs = []
                input_shapes = []
                for input_name in input_names:
#                    print(module_name, module)
                    inpt = self.get_output(input_name)
                    inputs += [inpt]
                    input_shapes += [inpt.shape]
                
#                print("Sequential forward", module_name, input_shapes)
                batch = module(*inputs)
            else:
#                print("Sequential forward", module_name, batch.shape if batch is not None else None)

#                print('Not multi', module.__class__)
                if index == 0:
                    batch = module(*args)
                else:
                    batch = module(batch)

            self.set_output(module_name, batch)
        self.set_output(None, batch)
        return batch

class SequentialGen(ContainerLayerGen):    
    def build_(self, input_size = None):
        od = collections.OrderedDict()

        seq = Sequential()

        for name, obj in self.enumerate_children():
            if name in seq._modules:
                raise Exception("Duplicated module name %s" % name)
            input_names = obj.get_input_names()
            if input_names != None:
                input_size = []
                for input_name in input_names:
#                    print("SequentialGen", name, input_name)
                    input_size += [self.get_output_size(input_name)]

            last_input_size = tuple(input_size) if input_size is not None else None
            layer, input_size = obj.build(input_size)
#            print(name, last_input_size, input_size)

            self.add_child_and_output_size(name, obj, input_size)
            if(name in od):
                raise Exception("Layer %s is already in sequence" % name)
            seq._modules[name] = layer
            set_layer_child_parent(layer, seq)
            
        return seq, input_size

