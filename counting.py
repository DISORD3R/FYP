from PIL import Image
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train16/weights/best.pt")

# change both to the image and its label
imageFile = "merge_augmented_v1.0/test/images/IMG_0535.JPG"
groundTruthFile = "merge_augmented_v1.0/test/labels/IMG_0535.txt"

results = model.predict(imageFile, verbose=False, conf=0.75)

# plot out the prediction result
for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    im.show()

# extract info that predicted
boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# iterate through the results
for box, cls, conf in zip(boxes, classes, confidences):
    x1, y1, x2, y2 = box
    confidence = conf
    name = names[int(cls)]

    width = x2 - x1
    height = y2 - y1

    print(f"Class: {name}, Confidence: {confidence:.2f}")
    print(f"Bounding Box: [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")
    print(f"Width: {width:.2f}, Height: {height:.2f}")
    print("---")