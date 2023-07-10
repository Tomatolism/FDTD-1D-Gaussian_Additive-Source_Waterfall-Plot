import cv2
import numpy as np
import random

def fill_white_area(point, image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to obtain binary mask
    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Invert the binary mask
    inverted_mask = cv2.bitwise_not(thresholded)

    # Compute the average intensity of the non-white area
    average_intensity = np.mean(gray, mask=inverted_mask)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over contours and check if the point is inside any of them
    for contour in contours:
        if cv2.pointPolygonTest(contour, point, False) >= 0:
            # Fill the contour with the average intensity
            cv2.drawContours(image, [contour], 0, (average_intensity, average_intensity, average_intensity), -1)
            break

# Set the input and output file names as variables
input_file = 'input_points.txt'
output_file = 'output_points.txt'
image_file = 'your_image.jpg'

# Load the image
image = cv2.imread(image_file)
height, width, _ = image.shape

# Load the points from the input file
points = []
with open(input_file, 'r') as file:
    for line in file:
        x_rel, y_rel = map(float, line.strip().split())
        x = int(x_rel * width)
        y = int(y_rel * height)
        points.append((x, y))

# Randomly select a point
selected_point = random.choice(points)

# Fill the white area with the average intensity of the non-white area
fill_white_area(selected_point, image)

# Remove the selected point from the list
points.remove(selected_point)

# Save the modified image
output_image_file = 'filled_image.jpg'  # Set the output image file name
cv2.imwrite(output_image_file, image)

# Save the updated points to the output file in YOLO format
with open(output_file, 'w') as file:
    for point in points:
        x_rel = point[0] / width
        y_rel = point[1] / height
        file.write(f"{x_rel} {y_rel}\n")

# Print the output image and file names
print("Output image file:", output_image_file)
print("Output points file:", output_file)
