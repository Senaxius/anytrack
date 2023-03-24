import torch
import numpy as np

data = [[1, 2], [3,4]]
x_data = torch.tensor(data)

# We move our tensor to the GPU if available
if torch.cuda.is_available():
  tensor = x_data.to('cuda')
  print(f"Device tensor is stored on: {tensor.device}")