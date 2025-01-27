import torch
print(torch.cuda.is_available())  # Should return True if GPU is accessible
print(torch.cuda.device_count())  # Number of available GPUs
print(torch.cuda.get_device_name(0))  # Name of your GPU
