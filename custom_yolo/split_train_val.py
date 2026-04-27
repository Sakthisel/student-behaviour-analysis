import os
import shutil
import random

# ==========================
# CONFIG
# ==========================
image_dir = "custom_yolo/dataset/images/all"
label_dir = "custom_yolo/dataset/labels/all"

train_img_dir = "custom_yolo/dataset/images/train"
val_img_dir = "custom_yolo/dataset/images/val"
train_label_dir = "custom_yolo/dataset/labels/train"
val_label_dir = "custom_yolo/dataset/labels/val"

split_ratio = 0.8

# ==========================
# CREATE FOLDERS
# ==========================
for d in [train_img_dir, val_img_dir, train_label_dir, val_label_dir]:
    os.makedirs(d, exist_ok=True)

# ==========================
# SPLIT FILES
# ==========================
all_images = sorted([f for f in os.listdir(image_dir) if f.endswith(".jpg")])
random.shuffle(all_images)
split_index = int(len(all_images) * split_ratio)

train_images = all_images[:split_index]
val_images = all_images[split_index:]

# ==========================
# MOVE TRAIN FILES
# ==========================
for img_file in train_images:
    shutil.copy(
        os.path.join(image_dir, img_file), os.path.join(train_img_dir, img_file)
    )
    label_file = img_file.replace(".jpg", ".txt")
    shutil.copy(
        os.path.join(label_dir, label_file), os.path.join(train_label_dir, label_file)
    )

# ==========================
# MOVE VAL FILES
# ==========================
for img_file in val_images:
    shutil.copy(os.path.join(image_dir, img_file), os.path.join(val_img_dir, img_file))
    label_file = img_file.replace(".jpg", ".txt")
    shutil.copy(
        os.path.join(label_dir, label_file), os.path.join(val_label_dir, label_file)
    )

print(f" Total images: {len(all_images)}")
print(f" Train: {len(train_images)}, Val: {len(val_images)}")
