# Road Lane Line Detection System (Project of Internship)

This project is based on OpenCV image processing techniques to detect lane lines on roads in both images and video feeds.

## Key Steps:
1. **Canny Edge Detection**: The image is first converted to grayscale, blurred, and processed using Canny edge detection to emphasize the edges of objects in the scene.
2. **Region of Interest (ROI)**: The image is masked to focus only on the area of interest (lanes), removing irrelevant parts of the image.
3. **Hough Transform**: Using the Hough Line Transform, the program detects line segments in the processed image that represent potential lane lines.
4. **Slope and Intercept Calculation**: Detected lines are averaged and categorized into left and right lanes based on their slope. Coordinates are generated for these lines.
5. **Overlaying Lane Lines**: The calculated lane lines are drawn on the original frame and displayed in real-time.

## Features:
- **Image Processing**: Supports lane detection on single images.
- **Video Processing**: Processes videos to detect lanes on each frame in real-time.
- **Customizable Parameters**: You can adjust thresholds for edge detection, minimum line length, and more.

## Usage:
1. **For Image Input**: 
   Uncomment the block that processes the `test_image.jpg` file.
2. **For Video Input**:
   The video processing code is activated by default, reading frames from the video file (`test.mp4`).

## Requirements:
- OpenCV
- NumPy

## How to Run:
1. Install the required libraries:  
   ```bash
   pip install opencv-python numpy

### Find the Test Video File Here : https://github.com/rslim087a/road-video
