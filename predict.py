from PIL import Image
from ultralytics import YOLO
import cv2

# load the YOLO model
model = YOLO("runs/detect/train16/weights/best.pt")

# specify file path
imageFile = "counting/Evaluation/IMG_0525.JPG"

# make prediction
results = model.predict(imageFile, verbose=False, conf=0.75)

# read image and get dimensions
image = cv2.imread(imageFile)
image_height, image_width, _ = image.shape

# plot the results on image
for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    im.show()

# extract prediction info
boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# repeat over every detected object and print its info
for i in range(len(boxes)):
    x1, y1, x2, y2 = boxes[i]
    width = x2 - x1
    height = y2 - y1
    class_name = names[int(classes[i])]
    confidence = confidences[i]

    print(f"Class: {class_name}, Confidence: {confidence:.2f}")
    print(f"Bounding Box: [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")
    print(f"Width: {width:.2f}, Height: {height:.2f}")
    print("---")



