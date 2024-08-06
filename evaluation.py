from PIL import Image
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train16/weights/best.pt")

# change both to the image and its label
imageFile = "counting/small bottle/images/IMG_0548.JPG"
groundTruthFile = "counting/small bottle/labels/IMG_0548.txt"

results = model.predict(imageFile, verbose=False, conf=0.75)
groundTruthList = []

# read image and get its dimension
image = cv2.imread(imageFile)
image_height, image_width, _ = image.shape

with open(groundTruthFile, "r") as file:
    for line in file.readlines():
        parts = line.strip().split()
        cls = int(parts[0])
        x_center, y_center, width, height = map(float, parts[1:])
        x_center *= image_width
        y_center *= image_height
        width *= image_width
        height *= image_height
        x1 = x_center - width / 2
        y1 = y_center - height / 2
        x2 = x_center + width / 2
        y2 = y_center + height / 2
        groundTruthList.append([cls, x1, y1, x2, y2])


# function to calculate iou
def iou_calculation(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # area of intersect
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # area of pred and act
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute iou
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


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
    detected_class = cls
    name = names[int(cls)]

    width = x2 - x1
    height = y2 - y1

    print(f"Class: {name}, Confidence: {confidence:.2f}")
    print(f"Bounding Box: [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")
    print(f"Width: {width:.2f}, Height: {height:.2f}")
    print("---")

    # calculate IoU
    max_iou = 0
    for gt in groundTruthList:
        gt_cls, gt_x1, gt_y1, gt_x2, gt_y2 = gt
        if gt_cls == detected_class:
            iou = iou_calculation([x1, y1, x2, y2], [gt_x1, gt_y1, gt_x2, gt_y2])
            # avoid cases when there are multiple same class object assign to wrong gt
            max_iou = max(max_iou, iou)

    print(f"Max IoU with ground truth: {max_iou:.2f}")
    print("---")
