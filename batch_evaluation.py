import os
from PIL import Image
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train16/weights/best.pt")

image_folder = "merge_augmented_v1.0/test/images"
label_folder = "merge_augmented_v1.0/test/labels"


# function to calculate IoU
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


# Iterate through all images and labels
iou_list = []
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.JPG'))]

for image_file in image_files:
    imageFile = os.path.join(image_folder, image_file)
    labelFile = os.path.join(label_folder, os.path.splitext(image_file)[0] + ".txt")

    # read image and get its dimensions
    image = cv2.imread(imageFile)
    image_height, image_width, _ = image.shape

    # read ground truth labels
    groundTruthList = []
    with open(labelFile, "r") as file:
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

    # predict using the model
    results = model.predict(imageFile, verbose=False, conf=0.75)

    # prediction result store into variable
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    # Initialize a dictionary to keep track of the highest IoU for each ground truth box
    best_iou_per_gt = {tuple(gt): 0 for gt in groundTruthList}
    used_gt_boxes = set()

    # Calculate IoU for each detected object
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        detected_class = cls

        best_iou = 0
        best_gt = None
        # only take the one with highest IoU as a single image might have multiple object in a same class
        for gt in groundTruthList:
            gt_cls, gt_x1, gt_y1, gt_x2, gt_y2 = gt
            if gt_cls == detected_class:
                iou = iou_calculation([x1, y1, x2, y2], [gt_x1, gt_y1, gt_x2, gt_y2])
                if iou > best_iou and tuple(gt) not in used_gt_boxes:
                    best_iou = iou
                    best_gt = tuple(gt)

        if best_gt is not None:
            best_iou_per_gt[best_gt] = max(best_iou_per_gt[best_gt], best_iou)
            used_gt_boxes.add(best_gt)

    # Append the best IoU values to the iou_list
    for gt, iou in best_iou_per_gt.items():
        if iou > 0:
            iou_list.append(iou)

# calculate and display evaluation result
average_iou = sum(iou_list) / len(iou_list) if iou_list else 0
min_iou = min(iou_list) if iou_list else 0
max_iou = max(iou_list) if iou_list else 0

print(f"Average IoU: {average_iou:.2f}")
print(f"Minimum IoU: {min_iou:.2f}")
print(f"Maximum IoU: {max_iou:.2f}")

