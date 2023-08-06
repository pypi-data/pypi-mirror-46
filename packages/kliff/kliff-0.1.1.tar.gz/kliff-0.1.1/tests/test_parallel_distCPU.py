# Training a model using multiple processes:
import torch
import torch.nn as nn
import torch.multiprocessing as mp
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(35)


def init_processes(rank, size, fn, backend='tcp'):
    """ Initialize the distributed environment. """
    os.environ['MASTER_ADDR'] = '127.0.0.1'
    os.environ['MASTER_PORT'] = '29500'
    dist.init_process_group(backend, rank=rank, world_size=size)
    fn(rank, size)


def loss_fn(pref, label):
    return torch.sum(torch.pow(pref - label, 2))


def train(model, tset):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for data, labels in tset:
        print('@@lable', labels)
        optimizer.zero_grad()
        loss_fn(model(data), labels).backward()
        optimizer.step()  # This will update the shared parameters


def create_dataset():
    X = torch.empty(20, 5).uniform_(0, 1)
    Y = np.asarray(np.atleast_2d(0.1 * np.arange(20)).T, dtype=np.float32)
    Y = torch.from_numpy(Y)
    dataset = TensorDataset(X, Y)
    dataset = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=0)
    return dataset


n_in = 5
n_h1 = 10
n_out = 1
model = nn.Sequential(nn.Linear(n_in, n_h1), nn.ReLU(), nn.Linear(n_h1, n_out))
model.share_memory()  # Required for 'fork' method to work

print('@@ params before:', model.parameters())
for i in model.parameters():
    print(i)
    break

init_processes()
dataset = create_dataset()
torch.distributed.init_process_group(backend='gloo')
model = torch.nn.DistributedDataParallelCPU(model)
train(model, dataset)


print('@@ params after:', model.parameters())
for i in model.parameters():
    print(i)
    break
