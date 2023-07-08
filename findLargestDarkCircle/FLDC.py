import cv2
import numpy as np

# Read the image
image = cv2.imread('your_image.jpg')

# Convert the image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
_, threshold = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Perform the Hough circle detection
circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=100)

# Find the largest circle based on radius
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    circles = sorted(circles, key=lambda x: x[2], reverse=True)

    if circles:
        (x, y, r) = circles[0]

        # Create a mask to black out the area outside the largest circle
        mask = np.zeros_like(image_gray)
        cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

        # Apply the mask to the original image
        result = cv2.bitwise_and(image, image, mask=mask)

        # Display the result
        cv2.imshow("Blackout Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
