import cv2
import numpy as np
import math

def getCircle(p1, p2, p3):
    x1, x2, x3 = p1[0], p2[0], p3[0]
    y1, y2, y3 = p1[1], p2[1], p3[1]

    center_x = (x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)
    center_x /= (2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2))

    center_y = (x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)
    center_y /= (2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2))

    radius = math.sqrt((center_x - x1) * (center_x - x1) + (center_y - y1) * (center_y - y1))

    return (center_x, center_y), radius

def getPointPositions(binaryImage):
    pointPositions = []
    rows, cols = binaryImage.shape

    for y in range(rows):
        for x in range(cols):
            if binaryImage[y, x] > 0:
                pointPositions.append((x, y))

    return pointPositions

def verifyCircle(dt, center, radius):
    counter = 0
    inlier = 0
    minInlierDist = 2.0
    maxInlierDistMax = 100.0
    maxInlierDist = radius / 25.0
    if maxInlierDist < minInlierDist:
        maxInlierDist = minInlierDist
    if maxInlierDist > maxInlierDistMax:
        maxInlierDist = maxInlierDistMax

    inlierSet = []

    for t in np.arange(0, 2 * math.pi, 0.05):
        counter += 1
        cX = radius * math.cos(t) + center[0]
        cY = radius * math.sin(t) + center[1]

        if 0 <= cX < dt.shape[1] and 0 <= cY < dt.shape[0] and dt[int(cY), int(cX)] < maxInlierDist:
            inlier += 1
            inlierSet.append((cX, cY))

    return inlier / counter, inlierSet

def evaluateCircle(dt, center, radius):
    completeDistance = 0.0
    counter = 0
    maxDist = 1.0
    minStep = 0.001

    step = 2 * math.pi / (6.0 * radius)
    if step < minStep:
        step = minStep

    for t in np.arange(0, 2 * math.pi, step):
        cX = radius * math.cos(t) + center[0]
        cY = radius * math.sin(t) + center[1]

        if 0 <= cX < dt.shape[1] and 0 <= cY < dt.shape[0] and dt[int(cY), int(cX)] <= maxDist:
            completeDistance += dt[int(cY), int(cX)]
            counter += 1

    return counter

# Load the image
color = cv2.imread('HoughCirclesAccuracy.png')

# Convert to grayscale
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

# Get binary image
mask = gray > 0

numberOfCirclesToDetect = 2

for j in range(numberOfCirclesToDetect):
    edgePositions = getPointPositions(mask)

    print("number of edge positions:", len(edgePositions))

    # Create distance transform
    dt = cv2.distanceTransform(255 - mask.astype(np.uint8), cv2.DIST_L1, 3)

    nIterations = 0
    bestCircleCenter = None
    bestCircleRadius = 0
    bestCVal = -1
    minCircleRadius = 0.0

    for i in range(2000):
        idx1 = np.random.randint(0, len(edgePositions))
        idx2 = np.random.randint(0, len(edgePositions))
        idx3 = np.random.randint(0, len(edgePositions))

        while idx2 == idx1:
            idx2 = np.random.randint(0, len(edgePositions))

        while idx3 == idx1 or idx3 == idx2:
            idx3 = np.random.randint(0, len(edgePositions))

        center, radius = getCircle(edgePositions[idx1], edgePositions[idx2], edgePositions[idx3])

        if radius < minCircleRadius:
            continue

        cVal = evaluateCircle(dt, center, radius)

        if cVal > bestCVal:
            bestCVal = cVal
            bestCircleRadius = radius
            bestCircleCenter = center

        nIterations += 1

    print("current best circle:", bestCircleCenter, "with radius:", bestCircleRadius, "and nInlier", bestCVal)
    cv2.circle(color, (int(bestCircleCenter[0]), int(bestCircleCenter[1])), int(bestCircleRadius), (0, 0, 255))

    mask = cv2.circle(mask, (int(bestCircleCenter[0]), int(bestCircleCenter[1])), int(bestCircleRadius), 0, 10)

cv2.namedWindow("edges")
cv2.imshow("edges", mask.astype(np.uint8) * 255)
cv2.namedWindow("color")
cv2.imshow("color", color)
cv2.imwrite("detectedCircles.png", color)
cv2.waitKey(-1)
