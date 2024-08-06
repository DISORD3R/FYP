from ultralytics import YOLO

# load the model
model = YOLO("yolov8s.yaml")

# checkpoint to continue from
checkpoint_path = "runs/detect/train13/weights/last.pt"

if __name__ == '__main__':
    # continue training
    model.train(data="config_trainingData2.0.yaml", epochs=40, device=0, resume=checkpoint_path)





