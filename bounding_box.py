import os
import cv2
import yaml

with open("data.yaml") as file:
    data = yaml.safe_load(file)

image_paths = data["train"]
annotation_paths = data["train_annotations"]
class_names = data["names"]
output_dir = "bb_images/"

def draw_bounding_box(image_path, annotation_path, output_path):
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    with open(annotation_path, 'r') as f:
        annotations = f.readlines()

    for ann in annotations:
        ann = ann.strip().split()
        
        if len(ann) == 0:
            print(f"Empty annotation found: {ann}")
            continue

        if len(ann) < 5:
            print(f"Incomplete annotation found: {ann}")
            continue
        
        try:
            class_id = int(ann[0])
            
        except ValueError:
            print(f"Non-integer class_id found: {ann[0]}")
            continue

        if class_id < 0 or class_id >= len(class_names):
            print(f"Invalid class_id {class_id} in file {annotation_path}")
            continue
        
        x_center = float(ann[1]) * w
        y_center = float(ann[2]) * h
        bbox_width = float(ann[3]) * w
        bbox_height = float(ann[4]) * h
        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, class_names[class_id], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    
    cv2.imwrite(output_path, image)

for image_dir, annotation_dir in zip(image_paths, annotation_paths):
    for annotation_file in os.listdir(annotation_dir):
        if annotation_file.endswith('.txt'):
            image_file_base = annotation_file.replace('.txt', '')  # Get base name without extension
            possible_extensions = ['.jpg', '.jpeg']
            image_path = None
            
            for ext in possible_extensions:
                if os.path.exists(os.path.join(image_dir, image_file_base + ext)):
                    image_path = os.path.join(image_dir, image_file_base + ext)
                    break
            
            if image_path:
                annotation_path = os.path.join(annotation_dir, annotation_file)
                image_filename = os.path.basename(image_path)
                output_path = os.path.join(output_dir, image_filename)
                
                draw_bounding_box(image_path, annotation_path, output_path)
            else:
                print(f"Image file for annotation {annotation_file} not found in {image_dir}")

print("Processing completed.")
