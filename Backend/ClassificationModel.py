# import torch
# from PIL import Image
# from torchvision import transforms

# loaded_model = torch.load("model_file1.pt")
# loaded_model.eval()

# # get image from frontend
# image = "IMAGE FROM FRONT"
# transform = transforms.Compose([
#     transforms.Resize((380, 380)),
#     transforms.CenterCrop(380),
#     transforms.ToTensor(),
#     # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])
# input_tensor = transform(image).unsqueeze(0)

# with torch.no_grad():
#     output = loaded_model(input_tensor)
#     predicted_class = output.argmax(dim=1).item()

# result_map = {0: "ClassA", 1: "ClassB", 2: "ClassC", 3: "ClassD"}
# print("Predicted class:", result_map[predicted_class])
