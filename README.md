# License Plate Recognition and Tracking

This project utilizes computer vision techniques to perform license plate recognition and vehicle tracking in a video. It uses the YOLOv8n model for vehicle detection and a custom model for license plate detection. The project is designed to process a video file named "sample.mp4" located in the selected folder.

## Setup

1. Clone the repository.
2. Install the required packages listed in `requirements.txt`.
3. Clone the 'sort' repository into the execution folder of the scripts from the following link: [https://github.com/abewley/sort.git](https://github.com/abewley/sort.git).
4. Ensure the selected folder contains a video file named "sample.mp4".

## Usage

1. Run the `main.py` script.
2. Select the folder containing the video file.
3. The program will process the video, detecting vehicles, tracking them, and recognizing license plates.
4. The results will be saved in a CSV file named `test_interpolated.csv` and an output video file named `out.mp4`.

## Results

The program outputs an annotated video with bounding boxes around vehicles and their respective license plates. The license plate numbers are also displayed on the video.

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- pandas
- sort (from `util`)

## Notes

- The program expects a specific video file name ("sample.mp4") in the selected folder. Please ensure the file is present before running the program.
- The `util` module contains helper functions for processing frames, drawing borders, and managing license plate recognition.
