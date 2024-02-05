from ultralytics import YOLO
import cv2

from sort.sort import *

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('models/license_plate_recognizer.pt')

# load video
cap = cv2.VideoCapture('cars-driving_1.mkv')

vehicles = [2, 3, 5, 7]  # car, bus, truck, motorbike


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
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])
        
        # track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_))
                

        # detecd license plates
        license_plates = detections = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
           

            

        # assign license plates to car

        # crop license plate

        # process license plate

        # read license plate number

        # write results