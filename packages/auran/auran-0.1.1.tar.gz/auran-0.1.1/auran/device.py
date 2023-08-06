import torch

device = None
cuda_enabled = False

def prepare_object(o):
    global device, cuda_enabled
    if device == None and cuda_enabled:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("Running on device", device)
        
    return o.to(device)

def prepare_numpy_object(o):
    return prepare_object(torch.FloatTensor(o))

def zeros(size):
    global device
    return torch.zeros(size, device = device)

def tensor(tensor, *args, **kwargs):
    ret = torch.tensor(tensor, *args, dtype=torch.float32, **kwargs)
    return prepare_object(ret)

def tensor2numpy(t):
    return t.cpu().data.numpy()



