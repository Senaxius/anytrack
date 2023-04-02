import pandas as pd
import numpy as np
import math
import torch
import random
from tqdm import tqdm
from torch import nn
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

class InputData(Dataset):
    def __init__(self, size=64, camera_count=2, pics=5):
        self.size = size
        self.camera_count = camera_count
        self.input = []
        self.target = []
        # generate random camera_poses (targets)
        for i in tqdm(range(size)):
            cam_pose = []
            for cam in range(camera_count - 1):
                x = random.randrange(-2000, 2000) / 1000
                y = random.randrange(-200, 200) / 1000
                z = random.randrange(0, 4000) / 1000
                position = [x, y, z]
                c = random.randrange(1500, 3000) / 1000
                ax = random.randrange(-1000, 1000) / 100 
                az = random.randrange(-1000, 1000) / 100 
                ay = round(angle((0-x,0-y,c-z), (0, 0, 1)) / math.pi * 180, 2)
                orientation = [ax, ay, az]
                if (x > 0):
                    ay *= -1
                cam_pose.append([position, orientation])
            self.target.append(cam_pose)
            
        # generate random input vectors (input)
        for pose in tqdm(self.target):
            inputs = []
            # generate multiple inputs for one pose
            for i in range(pics):
                pic = []
                for cam in range(camera_count):
                    if cam == 0:
                        px = (random.randrange(-600, 600) / 1000)
                        py = (random.randrange(-600, 600) / 1000)
                        pz = (random.randrange((c * 1000) - 600, (c * 1000) + 600) / 1000)
                    else:
                        px = (random.randrange(-600, 600) / 1000) - pose[cam - 1][0][0]
                        py = (random.randrange(-600, 600) / 1000) - pose[cam - 1][0][1]
                        pz = (random.randrange((c * 1000) - 600, (c * 1000) + 600) / 1000) - pose[cam - 1][0][2]
                    px = round(px, 2)
                    py = round(py, 2)
                    pz = round(pz, 2)
                    pic.append([px, py, pz])
                inputs.append(pic)
            self.input.append(inputs)
        
    def __len__(self):
        return len(self.input)

    def __getitem__(self, index):
        input = torch.tensor(self.input[index]).to("cuda:0")
        target = torch.tensor(self.target[index]).to("cuda:0")
        return input, target

    def get_input_size(self):
        input = torch.tensor(self.input[0])
        input = torch.flatten(input)
        return len(input)
    def get_target_size(self):
        target = torch.tensor(self.target[0])
        target = torch.flatten(target)
        return len(target)

class Calibrator_Network(nn.Module):
    def __init__(self):
        super().__init__()

        # Inputs

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    train_data = InputData(size=5000, camera_count=2, pics=5)
    test_data = InputData(size=100, camera_count=2, pics=5)

    train_dataloader = DataLoader(train_data, batch_size=1, shuffle=False)
    test_dataloader = DataLoader(test_data, batch_size=1, shuffle=False)

    input_size = train_data.get_input_size()
    output_size = train_data.get_target_size()
    hidden_sizes = [40, 35, 12]

    model = nn.Sequential(
        nn.Linear(input_size*1, hidden_sizes[0]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[0], hidden_sizes[1]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[1], hidden_sizes[2]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[2], output_size*1),
    )

    # print(model)
    # input, target = next(iter(train_dataloader))
    # print(target[0])

    # Define the loss
    criterion = nn.L1Loss()
    criterion = criterion.cuda()
    # Optimizers require the parameters to optimize and a learning rate
    optimizer = optim.SGD(model.parameters(), lr=0.003)    

    model = model.cuda()

    # for i in model.parameters():
    #     print(i.is_cuda)
    

    epochs = 100
    for e in range(epochs):
        running_loss = 0
        for input, target in tqdm(train_dataloader):
            input = torch.flatten(input).cuda()
            target = torch.flatten(target).cuda()
            target = target.type(torch.LongTensor).cuda()

            # Training pass
            optimizer.zero_grad()
            
            output = model(input)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        else:
            print(f"Training loss: {running_loss/len(train_dataloader)}")
    
    input, target = next(iter(test_dataloader))
    input = torch.flatten(input)
    output = model(input)
    print(output)

    target = target.type(torch.LongTensor)
    print(target)


    # input_tensor = torch.zeros((5, 2, 3), dtype=torch.float32)
    # print(input_tensor)