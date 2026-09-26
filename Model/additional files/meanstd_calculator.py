import numpy as np
import cv2
import os
from tqdm import tqdm

IMAGES_PATH = r'C:\Users\aquas\Jupyter\ML_Project_git\dataset\train'
pixel_sum, pixel_squared_sum, pixel_count = np.zeros(3, dtype=np.float64), np.zeros(3, dtype=np.float64), 0

files_list = [os.path.join(root, file) for root, _, files in os.walk(IMAGES_PATH) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

os.system('cls')
for file_path in tqdm(files_list, desc="Processing images", unit="image"):
    img = cv2.imread(file_path)
    if img is not None:
        img_resized = cv2.resize(img, (380, 380)) / 255.0
        pixel_sum += np.sum(img_resized, axis=(0, 1))
        pixel_squared_sum += np.sum(img_resized ** 2, axis=(0, 1))
        pixel_count += img_resized.shape[0] * img_resized.shape[1]

mean_np = pixel_sum / pixel_count
std_np = np.sqrt(pixel_squared_sum / pixel_count - mean_np ** 2)

with open(r'C:\Users\aquas\Jupyter\ML_Project_git\MLproject\helper files\meanstd.txt', 'w') as file:
    file.write(f"Mean: {mean_np.tolist()}\n")
    file.write(f"Standard Deviation: {std_np.tolist()}\n")

print("Mean and standard deviation written to file.")

# Mean: [0.2954581669589034, 0.29541042352786206, 0.29537371119537875]
# Standard Deviation: [0.31727746077062646, 0.31729778651393764, 0.31726590300772206]