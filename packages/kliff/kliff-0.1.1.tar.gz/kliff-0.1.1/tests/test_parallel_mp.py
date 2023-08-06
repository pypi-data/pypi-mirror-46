# Training a model using multiple processes:
import torch
import torch.nn as nn
import torch.multiprocessing as mp
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(35)


X = torch.empty(20, 5).uniform_(0, 1)
Y = np.asarray(np.atleast_2d(0.1 * np.arange(20)).T, dtype=np.float32)
Y = torch.from_numpy(Y)
dataset = TensorDataset(X, Y)
dataset = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=0)


def loss_fn(pref, label):
    return torch.sum(torch.pow(pref - label, 2))


def train(model, tset):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for data, labels in tset:
        print('@@lable', labels)
        optimizer.zero_grad()
        loss_fn(model(data), labels).backward()
        optimizer.step()  # This will update the shared parameters


n_in = 5
n_h1 = 10
n_out = 1
model = nn.Sequential(nn.Linear(n_in, n_h1), nn.ReLU(), nn.Linear(n_h1, n_out))
model.share_memory()  # Required for 'fork' method to work

print('@@ params before:', model.parameters())
for i in model.parameters():
    print(i)
    break

processes = []
# for i in range(mp.cpu_count()):  # No. of processes
for i in range(1):  # No. of processes
    print('@@@ cpu i', i)
    p = mp.Process(target=train, args=(model, dataset))
    p.start()
    processes.append(p)
for p in processes:
    p.join()
print('@@ params after:', model.parameters())
for i in model.parameters():
    print(i)
    break
