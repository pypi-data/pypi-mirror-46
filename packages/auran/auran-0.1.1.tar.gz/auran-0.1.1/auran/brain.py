from . import organism, xp, ann, device
import numpy
import torch
import torch.nn as nn
from torch.autograd import Variable
import math
import os
import copy
import json
import shutil

class Hook():
    def __init__(self, module, backward=False):
        if backward==False:
            self.hook = module.register_forward_hook(self.hook_fn)
        else:
            self.hook = module.register_backward_hook(self.hook_fn)
        self.input = None
        self.output = None
        
    def hook_fn(self, module, input, output):
        self.input = input
        self.output = output
        
    def close(self):
        self.hook.remove()

class Net(nn.Module):
    state_sizes = []
    # input_sizes contains the size of all the inputs
    def __init__(self, xp, input_sizes, bare = False, *args, **kwargs):
        super(Net, self).__init__()
        self.xp = xp

        self.args = args
        self.kwargs = kwargs

        # Make sure input and state sizes have the right type
        self.input_sizes = self.size_sanitize(input_sizes)
        self.state_sizes = self.size_sanitize(self.get_state_sizes())

        # Create inputs/states holders : X input will be accessible through Inputs.X , and X state will be accessible through State.X
        self.inputs_gen = self.holder_create(self.input_sizes)
        self.states_gen = self.holder_create(self.state_sizes)
        
        # Build the network object, passing it the input_sizes and the generator for inputs
        self.network, output_size = self.get_network()

#        print(self.network, output_size)
        
        self.get_states()
        self.add_backward_hook()
        
        assert(isinstance(self.network, ann.Sequential))
        
        device.prepare_object(self.network)
        if not bare:
            self.prepare()

        if hasattr(self, "output_size"):
            if(output_size != self.output_size):
                raise Exception("Invalid size %s compared to declared one %s " % (output_size, self.output_size))

        self.output_size = output_size
        self.output_reset()
        self.state_reset()

    def enumerate_modules_rec(self, root, prefix = "", terminal_only = True):
        is_container = isinstance(root, ann.ContainerLayer)
        
        if not is_container or not terminal_only:
            if prefix != "":
                yield prefix
                
        if not is_container:
            return
        
        for module_name, module in root._modules.items():
            if prefix != "":
                new_prefix = prefix + "." + module_name
            else:
                new_prefix = module_name

            for r in self.enumerate_modules_rec(module, prefix = new_prefix, terminal_only = terminal_only):
                yield r
            
    def get_network(self):
        # Build the top level sequence, prefixed by state definition and input definition
        seq_gen_children = []
        if len(self.state_sizes) != 0:
            seq_gen_children += [("State", self.states_gen)]
        seq_gen_children += [("Inputs", self.inputs_gen)]
        seq_gen_children += self.get_sequence()                
        seq_gen = ann.SequentialGen(*seq_gen_children)

        return seq_gen.build()

    def get_states(self):
        self.states = []
        for n in self.enumerate_modules_rec(self.network, terminal_only = False):
            if n.split(".")[-1] == "State":
                self.states += [n]

    def add_backward_hook(self):
        self.hooks = {}
        for name in self.enumerate_modules_rec(self.network, terminal_only = True):
            module = self.network.get_module(name)
            self.hooks[name] = Hook(module,backward=True)

    def get_state_sizes(self):
        return self.state_sizes
        
    def size_sanitize(self, sizes):
        s = []
        if isinstance(sizes, list) or isinstance(sizes, tuple):
            enumerator = sizes
        elif isinstance(sizes, dict):
            enumerator = sizes.items()
        else:
            raise Exception("Unknown type for sizes:", sizes)
        for name, size in enumerator:
            if not isinstance(size, int):
                assert(isinstance(size, list) or isinstance(size, tuple))
                size = [int(s) for s in size]
            else:
                size = (size,)
            s += [(name, size)]
#        print("size_sanitize output", s)
        return s
    
    def holder_create(self, sizes):
        holders_gen = [(name, ann.TensorHolderGen(size)) for name, size in sizes]
        return ann.BroadcastGen(*holders_gen)        

    def set_input(self, name, value):
        constant_holder = self.network._modules["Inputs"].get_module(name)
        constant_holder.set(value)

    def get_input(self, name):
        constant_holder = self.network._modules["Inputs"].get_module(name)
        return constant_holder.get()
        
    def display(self, xp, timestamp):
        for name, m in self._modules.items():
            if isinstance(m, ann.ContainerLayer):
                m.display(xp, timestamp)
        for module_name, hook in self.hooks.items():
            if hook.input is None:
                continue
            
            for t_index, t in enumerate(hook.input):
                if t is not None:
                    display_name = "net." + module_name + "#b%s" % t_index
#                    print(display_name, t_index, t.shape)
                    xp.add_display(timestamp, display_name, t.cpu().data.clone().numpy())
#            print(module_name, hook.input)

    def get_output(self):
        if not hasattr(self, "net_output"):
            self.output_reset()

        return self.net_output

    def output_reset(self):
        batch_output_size = (1,) + self.output_size
        self.net_output = device.zeros(batch_output_size)

    def state_reset(self):
        for state_name in self.states:
            holder = self.network.get_module(state_name)
        
            for tensor_holder_name, tensor_holder in holder._modules.items():
                tensor_holder.reset()                
                
    def forward(self):
        self.net_output = self.network()
        return self.net_output

    def prepare(self):
        # Do some final work, like adding some layers, for example for recurring networks when used standalone,
        # and not in combination with other networks
        pass

    def save(self, path):
        # TEMPORARY
        return        
        net_path = os.path.join(path, "network")
        with open(net_path, "wb") as f :
            torch.save(self, f)

        statedict_path = os.path.join(path, "statedict")
        with open(statedict_path, "wb") as f:
            torch.save(self.state_dict(), f)

        meta_path = os.path.join(path, "meta")
        xp_name = self.xp.get_xp_module()
        meta_dict = {"input_sizes":list(self.input_sizes),
                     "output_size":list(self.output_size), "xp_module":xp_name}
        if self.state_sizes != None:
            meta_dict["state_sizes"] = self.state_sizes
        
        with open(meta_path, "w") as f:
            f.write(json.dumps(meta_dict))

    def load(self, path = None):
        # If no path is given, load the latest network trained for this experiment
        if path == None:
            path = self.xp.get_latest_path()
        print("Net loading from %s" % path)
        # From https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-model-for-inference
        with open(os.path.join(path, "statedict"), "rb") as f:
            state_dict =  torch.load(f)
        self.load_state_dict(state_dict, strict = True)

    @staticmethod
    def network_create(path, *args, **kwargs):
        meta_path = os.path.join(path, "meta")
        with open(meta_path, "r") as f:
            meta = json.loads(f.read())
        xp_module_name = meta["xp_module"]

        import importlib
        module = importlib.import_module(xp_module_name)
        # This is needed when using live coding stuff, otherwise the module is cached and the module.Net() constructor triggers an error
        importlib.reload(module)
        inputs_size = meta["inputs_size"]
        net = module.Net(None, inputs_size, *args, **kwargs)
        if "states_size" in meta:
            net.states_size = meta["states_size"]        

        return net

    @staticmethod
    def network_output_size(path, *args, **kwargs):
        net = Net.network_create(path, *args, **kwargs)
        return net.output_size

    @staticmethod
    def network_create_and_load(path, *args, **kwargs):
        net = Net.network_create(path, *args, **kwargs)
        net.load(path)

        return net

class Brain(organism.Organ):
    def __init__(self, world, translation, net):
        super(Brain, self).__init__(world, translation, "brain")
        self.net = net
        
    def run(self, timestamp):
        self.output = device.tensor2numpy(self.net.forward()).flatten()
        
    def set_input(self, name, value):
        value = device.tensor(value)
        self.net.set_input(name, value)

    def get_input(self, name):
        return self.net.get_input(name)
        
    def get_output(self, name):
        if name == "hand":
            ret = numpy.array(self.output)[:2]
            return ret
        elif name == "eye":
            ret = numpy.array(self.output)[:2]
            return ret
        elif name == "eye_confidence":
            return None
            out = numpy.array(self.output)
            if out.shape[0] > 2:
                ret = math.sqrt(math.exp(out[2]))
            else:
                ret = None
            return ret

    def save(self, path):
        self.net.save(path)

    def reset(self):
        self.net.output_reset()
        self.net.state_reset()

