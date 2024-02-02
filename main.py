from ultralytics import YOLO
import cv2


# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('models/license_plate_recognizer.pt')

# load video
cap = cv2.VideoCapture('cars.driving_1.mkv')

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret and frame_nmr < 10:
        pass
        # detect vehicles
        detections = coco_model(frame)[0]
        print(detections)

        # track vehicles

        # detecd license plates

        # assign license plates to car

        # crop license plate

        # process license plate

        # read license plate number

        # write results