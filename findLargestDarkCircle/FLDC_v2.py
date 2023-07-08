import cv2
import numpy as np

# Read the image
image = cv2.imread('your_image.jpg')

# Convert the image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to create a binary mask of dark regions
_, mask = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Perform connected component analysis on the mask
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

# Find the index of the largest connected component (excluding background)
largest_component_index = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

# Create a mask to isolate the largest component
largest_component_mask = np.uint8(labels == largest_component_index) * 255

# Apply the largest component mask to the original image
image_filtered = cv2.bitwise_and(image, image, mask=largest_component_mask)

# Convert the filtered image to grayscale
filtered_gray = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)

# Perform Hough circle detection on the filtered image
circles = cv2.HoughCircles(filtered_gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=100)

# Draw circles for each detected circle
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        # Draw the circle outline
        cv2.circle(image_filtered, (x, y), r, (0, 255, 0), 2)
        # Draw the center of the circle
        cv2.circle(image_filtered, (x, y), 2, (0, 0, 255), 3)

# Display the image with the largest non-dark area and detected circles
cv2.imshow("Filtered Image with Circles", image_filtered)
cv2.waitKey(0)
cv2.destroyAllWindows()
