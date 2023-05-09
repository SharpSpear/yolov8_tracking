from ultralytics import YOLO

model_path = "weights/yolov8n.pt"

vid_path = "videos/video_1.mp4"

# Load Pre-trained ML Model
model = YOLO(model_path)

results = model.track(vid_path,
                      conf=0.3,
                      iou=0.5,
                      show=True
                      )