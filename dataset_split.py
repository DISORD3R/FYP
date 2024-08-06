import os
import shutil
import random


def create_folders(base_path):
    folders = ['train', 'test', 'val']
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(base_path, folder, 'labels'), exist_ok=True)


def split_data(images_path, labels_path, base_path, train_ratio=0.8, test_ratio=0.1, valid_ratio=0.1):
    images = os.listdir(images_path)
    random.shuffle(images)

    train_split = int(train_ratio * len(images))
    test_split = int(test_ratio * len(images))
    valid_split = len(images) - train_split - test_split

    train_images = images[:train_split]
    test_images = images[train_split:train_split + test_split]
    valid_images = images[train_split + test_split:]

    move_files(train_images, images_path, labels_path, os.path.join(base_path, 'train'))
    move_files(test_images, images_path, labels_path, os.path.join(base_path, 'test'))
    move_files(valid_images, images_path, labels_path, os.path.join(base_path, 'val'))


def move_files(files, images_path, labels_path, dest_path):
    for file in files:
        image_src = os.path.join(images_path, file)
        label_src = os.path.join(labels_path, file.replace('.jpg', '.txt').replace('.JPG', '.txt'))

        image_dest = os.path.join(dest_path, 'images', file)
        label_dest = os.path.join(dest_path, 'labels', os.path.basename(label_src))

        shutil.copy(image_src, image_dest)
        shutil.copy(label_src, label_dest)


if __name__ == "__main__":
    images_path = 'merge_augmented_v1.0/images'
    labels_path = 'merge_augmented_v1.0/labels'
    base_path = 'merge_augmented_v1.0'

    create_folders(base_path)
    split_data(images_path, labels_path, base_path)



