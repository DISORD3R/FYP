import os
import cv2

# paths to the image and label directories
image_dirs = ["collected_data_merge/train/images"]
label_dirs = ["collected_data_merge/train/labels"]

flipped_base_dir = 'collected_data_merge/augment(mirror)'
flipped_image_dirs = os.path.join(flipped_base_dir, 'images')  # Corrected to string
flipped_label_dirs = os.path.join(flipped_base_dir, 'labels')  # Corrected to string

# create directories if they don't exist
os.makedirs(flipped_image_dirs, exist_ok=True)
os.makedirs(flipped_label_dirs, exist_ok=True)

def flip_image_and_labels(image_path, label_path, save_image_path, save_label_path):
    # Read image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Flip image horizontally
    flipped_image = cv2.flip(image, 1)

    # Save flipped image
    cv2.imwrite(save_image_path, flipped_image)

    # Read and flip labels
    with open(label_path, 'r') as file:
        lines = file.readlines()

    flipped_lines = []
    for line in lines:
        parts = line.strip().split()
        class_id = parts[0]
        x_center = float(parts[1])
        y_center = float(parts[2])
        bbox_width = float(parts[3])
        bbox_height = float(parts[4])

        # Calculate new x_center after flip
        new_x_center = 1.0 - x_center

        # Adjust if necessary based on label format (e.g., YOLO format)
        # new_x_center = width - x_center - 1

        flipped_line = f"{class_id} {new_x_center} {y_center} {bbox_width} {bbox_height}\n"
        flipped_lines.append(flipped_line)

    # Save flipped labels
    with open(save_label_path, 'w') as file:
        file.writelines(flipped_lines)

def process_datasets(image_dirs, label_dirs, flipped_image_dirs, flipped_label_dirs):
    for image_dir, label_dir in zip(image_dirs, label_dirs):
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg"):
                image_path = os.path.join(image_dir, filename)
                label_path = os.path.join(label_dir, filename.replace('.jpg', '.txt'))

                # Define paths to save the flipped image and label
                save_image_path = os.path.join(flipped_image_dirs, f"{filename.replace('.jpg', '_flipped.jpg')}")
                save_label_path = os.path.join(flipped_label_dirs, f"{filename.replace('.jpg', '_flipped.txt')}")

                # Process the image and labels
                flip_image_and_labels(image_path, label_path, save_image_path, save_label_path)

# Process both datasets to create horizontally flipped images and corresponding labels
process_datasets(image_dirs, label_dirs, flipped_image_dirs, flipped_label_dirs)

