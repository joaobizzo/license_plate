from ultralytics import YOLO
import cv2

from sort.sort import *

from util import get_car, read_license_plate

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_recognizer_path = "../../../MODELS/license_plate_detector.pt"
license_plate_detector = YOLO(license_plate_recognizer_path)

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
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
           

            

        # assign license plates to car
        xcar1, ycar2, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        # crop license plate
        license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]

        # process license plate
        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        _, license_plate_crop_tresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

        # read license plate number


        # write results