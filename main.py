from ultralytics import YOLO
import cv2


# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('models/license_plate_recognizer.pt')

# load video
cap = cv2.VideoCapture('cars.driving_1.mkv')

# read frames
ret = True
while ret:
    ret, frames = cap.read()
    if ret:
        pass
        # detect vehicles

        # track vehicles

        # detecd license plates

        # assign license plates to car

        # crop license plate

        # process license plate

        # read license plate number

        # write results