# Imports for frontend
import sys
import os
import json
import ast
# Imports for normalization
import cv2
import numpy as np
from typing import Tuple
# Imports for model
import torch
from torchvision import transforms, datasets
from PIL import Image


# Find mean and standrt deviation values
def get_normalization_values(image: str) -> Tuple[np.ndarray, np.ndarray]:
    img = cv2.imread(image)
    img_resized = cv2.resize(img, (380, 380)) / 255.0
    pixel_count = img_resized.shape[0] * img_resized.shape[1]
    pixel_sum = np.sum(img_resized, axis=(0, 1))
    pixel_squared_sum = np.sum(img_resized ** 2, axis=(0, 1))
    
    mean_np = pixel_sum / pixel_count
    std_np = np.sqrt(pixel_squared_sum / pixel_count - mean_np ** 2)

    return mean_np, std_np


# Model loading, processing image and returning string with class
def call_model(image_path) -> str: # recive image location
    loaded_model = torch.load("model_99_acc.pt", map_location=torch.device('cpu'), weights_only=False)
    loaded_model.eval()

    mean_np, std_np = get_normalization_values(image_path)

    transform = transforms.Compose([
        transforms.Resize((380, 380)),
        transforms.CenterCrop(380),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean_np, std=std_np)
    ])
    image = Image.open(image_path) 

    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = loaded_model(input_tensor)
        predicted_class = output.argmax(dim=1).item()

    result_map = {0: "Stage 2", 1: "Stage 3", 2: "Healthy", 3: "Stage 1"} # define classes for used dataset
    result_class = result_map[predicted_class]

    return result_class

# This is temporary file instead of the model
route = ast.literal_eval(sys.argv[1])

if route == "process":
    message = call_model(f"uploads/Healthy.jpg")
else:
    message = "Invalid route!"

print(message)

uploads_folder = os.path.join(os.path.dirname(__file__), 'uploads')

sys.stdout.flush()