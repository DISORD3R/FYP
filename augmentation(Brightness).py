import os
from PIL import Image
from torchvision import transforms


def adjust_brightness(input_image_path, output_image_path, factor):
    img = Image.open(input_image_path)
    transform = transforms.ColorJitter(brightness=factor)
    img_transformed = transform(img)
    img_transformed.save(output_image_path)


def process_directory(input_dir, output_dir, brightness_factor):
    images_dir = os.path.join(input_dir, 'images')
    labels_dir = os.path.join(input_dir, 'labels')
    output_images_dir = os.path.join(output_dir, 'images')
    output_labels_dir = os.path.join(output_dir, 'labels')

    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    # augment every single image within the folder
    for img_file in os.listdir(images_dir):
        # validate
        if img_file.endswith('.jpg'):
            img_path = os.path.join(images_dir, img_file)
            ori, ext = os.path.splitext(img_file)
            #  rename the img file
            new_img_file = f"{ori}_bright{ext}"
            output_img_path = os.path.join(output_images_dir, new_img_file)

            adjust_brightness(img_path, output_img_path, brightness_factor)

            label_file = f"{ori}.txt"
            label_path = os.path.join(labels_dir, label_file)
            if os.path.exists(label_path):
                new_label_file = f"{ori}_bright.txt"
                output_label_path = os.path.join(output_labels_dir, new_label_file)
                with open(label_path, 'r') as src, open(output_label_path, 'w') as dst:
                    dst.write(src.read())


input_directory = 'collected_data_merge/train'
output_directory = 'collected_data_merge/augment(brightness2)'
brightness_factor = 0.8
process_directory(input_directory, output_directory, brightness_factor)
