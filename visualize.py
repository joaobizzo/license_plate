import ast
import cv2
import numpy as np
import pandas as pd
import time  # Import the time module
from os import system


def clear():
    system('clear')

def rgb_to_bgr(rgb):
    return (rgb[2], rgb[1], rgb[0])

border_color = (116, 226, 145)

rectangle_color = rgb_to_bgr((255, 0, 77))


def draw_border(img, top_left, bottom_right, color=(255, 0, 0), thickness=6, line_length_x=180, line_length_y=180):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)

    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)  #-- bottom-left
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)  #-- top-right
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)

    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)  #-- bottom-right
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img


def processing_animation(i):
    j = i % 4
    clear()
    print(f"Processing license plates{'.' * j}")
    #time.sleep(0.4)

# Load the data
results = pd.read_csv('./test_interpolated.csv')

# Setup video capture and writer
video_path = '../data/UK1/sample.mp4'
cap = cv2.VideoCapture(video_path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('../data/UK1/out.mp4', fourcc, fps, (width, height))

# calculate duration of the video 
seconds = round(frames / fps)

license_plate = {}
i=0
for car_id in np.unique(results['car_id']):
    max_ = np.amax(results[results['car_id'] == car_id]['license_number_score'])
    license_plate[car_id] = {
        'license_crop': None,
        'license_plate_number': results[(results['car_id'] == car_id) & (results['license_number_score'] == max_)]['license_number'].iloc[0]
    }
    cap.set(cv2.CAP_PROP_POS_FRAMES, results[(results['car_id'] == car_id) & (results['license_number_score'] == max_)]['frame_nmr'].iloc[0])
    ret, frame = cap.read()

    x1, y1, x2, y2 = ast.literal_eval(results[(results['car_id'] == car_id) & (results['license_number_score'] == max_)]['license_plate_bbox'].iloc[0].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))

    license_crop = frame[int(y1):int(y2), int(x1):int(x2)]
    license_crop = cv2.resize(license_crop, (int((x2 - x1) * 400 / (y2 - y1)), 400))

    license_plate[car_id]['license_crop'] = license_crop
    processing_animation(i)
    i+=1



frame_nmr = -1
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Start timing here
start_time = time.time()

# Process video frames
ret = True
while ret:
    ret, frame = cap.read()
    frame_nmr += 1
    if ret:
        df_ = results[results['frame_nmr'] == frame_nmr]
        for row_indx in range(len(df_)):
            car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(df_.iloc[row_indx]['car_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), border_color, 16, line_length_x=170, line_length_y=170)

            x1, y1, x2, y2 = ast.literal_eval(df_.iloc[row_indx]['license_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), rectangle_color, 10)

            license_crop = license_plate[df_.iloc[row_indx]['car_id']]['license_crop']

            H, W, _ = license_crop.shape
            try:
                frame[int(car_y1) - H - 100:int(car_y1) - 100, int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2)] = license_crop
                frame[int(car_y1) - H - 400:int(car_y1) - H - 100, int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2)] = (255, 255, 255)

                (text_width, text_height), _ = cv2.getTextSize(license_plate[df_.iloc[row_indx]['car_id']]['license_plate_number'], cv2.FONT_HERSHEY_SIMPLEX, 4.3, 17)

                cv2.putText(frame, license_plate[df_.iloc[row_indx]['car_id']]['license_plate_number'], (int((car_x2 + car_x1 - text_width) / 2), int(car_y1 - H - 250 + (text_height / 2))), cv2.FONT_HERSHEY_SIMPLEX, 4.3, (0, 0, 0), 17)
            except Exception as e:
                print(f"Error processing frame: {e}")

        
        out.write(frame)
        percent = frame_nmr / frames * 100
        time_left = ((100 - percent) / 100) * seconds
        min = int(time_left // 60)
        sec = int(time_left % 60)
        
        
        clear()
        print(f"{percent:.2f}%")
        if min > 0:
            print(f"{min} minutes and {sec} seconds left to process")
        else:
            print(f"{sec} seconds left to process.")
clear()
# Stop timing and print elapsed time
elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print("100% processed.")
if minutes > 0:
    print(f"Process completed in {minutes} minutes and {seconds} seconds.")
else:
    print(f"Process completed in {seconds} seconds.")
print("Video output successfuly saved to file.")

out.release()
cap.release()
