from PIL import Image
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train15/weights/best.pt")

metrics = model.val(data="config_merge_augmented_v1.0.yaml", workers=0)

print("map:", metrics.box.map75)


