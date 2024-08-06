import os
# used to remove those label file that does not have their respective image in the images folder


def remove_labels(images_dir, labels_dir):
    for label_file in os.listdir(labels_dir):
        if label_file.endswith('.txt'):
            base_name = os.path.splitext(label_file)[0]
            img_file_jpg = f"{base_name}.jpg"

            img_exists = os.path.exists(os.path.join(images_dir, img_file_jpg))

            if not img_exists:
                label_path = os.path.join(labels_dir, label_file)
                os.remove(label_path)
                print(f"Deleted orphan label file: {label_path}")


# change the directory here
images_directory = 'collected_data_merge/augment(brightness)/images'
labels_directory = 'collected_data_merge/augment(brightness)/labels'
remove_labels(images_directory, labels_directory)
