import cv2
import numpy as np

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))  # Slightly above the bottom of the image
    try:
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])
    except ZeroDivisionError:
        return None

def average_slope_intercept(image, lines):
    left_fit = []
    middle_fit = []
    right_fit = []

    if lines is None:
        return np.array([])

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)  # Get slope and intercept
        slope = parameters[0]
        intercept = parameters[1]

        if slope < -0.5:  # Steeper negative slope for left lane
            left_fit.append((slope, intercept))
        elif slope > 0.5:  # Positive slope for right lane
            right_fit.append((slope, intercept))
        else:  # Nearly vertical lines (for middle lane)
            middle_fit.append((slope, intercept))

    output_lines = []

    if left_fit:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_coordinates(image, left_fit_average)
        if left_line is not None:
            output_lines.append(left_line)

    if middle_fit:
        middle_fit_average = np.average(middle_fit, axis=0)
        middle_line = make_coordinates(image, middle_fit_average)
        if middle_line is not None:
            output_lines.append(middle_line)

    if right_fit:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_average)
        if right_line is not None:
            output_lines.append(right_line)

    return np.array(output_lines)

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(100, height), (image.shape[1] - 100, height), (image.shape[1] // 2, int(height * 0.55))]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return line_image

# Process video for lane detection
cap = cv2.VideoCapture('test2.mp4')  # Replace with your video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow('Lane Detection on Video', combo_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
