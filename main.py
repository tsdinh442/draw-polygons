import cv2
import numpy as np

vertices = []
polygons = []
n = 0
exe = False
stroke = 5


def draw_polygons(event, x, y, flags, params):
    global vertices
    global polygons
    global n
    global exe

    img = image.copy()

    # check if left click and first point
    if event == cv2.EVENT_LBUTTONDOWN and len(vertices) == 0:
        vertices.append((x, y))
        # draw the first point
        cv2.circle(img, (x, y), radius=stroke//2, color=(0, 255, 0), thickness=-1)
        cv2.imshow('polygons', img)

    elif event == cv2.EVENT_LBUTTONDOWN and len(vertices) < 2:
        vertices.append((x, y))
        # draw the first line
        cv2.line(img, vertices[0], vertices[-1], color=(0, 255, 0), thickness=stroke)
        n += 1
        cv2.imshow('polygons', img)

    # check if left_click and the point not close to the first point
    elif event == cv2.EVENT_LBUTTONDOWN and len(vertices) >= 2 and np.linalg.norm(np.array((x, y))
                                                                                 - np.array(vertices[0])) > 30:
        vertices.append((x, y))
        # cv2.circle(img, (x, y), radius=2, color=(0, 255, 0), thickness=-1)
        # draw a line connecting the new point and the previous point
        cv2.polylines(img, np.array([vertices]), isClosed=False, color=(0, 255, 0), thickness=stroke)
        n += 1
        cv2.imshow('polygons', img)

    # check if the click is the same or close to the first point
    elif event == cv2.EVENT_LBUTTONDOWN and np.linalg.norm(np.array((x, y)) - np.array(vertices[0])) <= 30:
        # close the polyline
        if len(vertices) > 2:
            cv2.polylines(image, np.array([vertices]), isClosed=True, color=(0, 0, 255), thickness=stroke)
            polygons.append(np.array(vertices, dtype=np.int32))
            cv2.imshow('polygons', image)
            vertices = []
            n = 0

    # check if right click
    elif event == cv2.EVENT_RBUTTONDOWN:
        vertices.pop()
        if len(vertices) == 1:
            cv2.circle(img, vertices[0], radius=stroke//2, color=(0, 255, 0), thickness=-1)
        else:
            cv2.polylines(img, np.array([vertices]), isClosed=False, color=(0, 255, 0), thickness=stroke)
            n -= 1
        cv2.imshow('polygons', img)


image = cv2.imread('city_street.jpg')

cv2.imshow('polygons', image)
cv2.setMouseCallback('polygons', draw_polygons)

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == 13:  # Check for Enter key press

        if len(polygons) > 0:
            exe = bool(input("Crop the image? "))

        if exe:
            blank = np.ones_like(image, dtype=np.uint8) * 255
            mask = np.zeros_like(image, dtype=np.uint8)
            cv2.fillPoly(mask, polygons, (255, 255, 255))

            opacity = 0.5
            blended = cv2.addWeighted(image, opacity, blank, 1 - opacity, 0)
            result = cv2.bitwise_and(blended, 255 - mask) + cv2.bitwise_and(image, cv2.bitwise_not(255 - mask))

            cv2.imshow('polygons', result)

        cv2.setMouseCallback('polygons', draw_polygons)


cv2.waitKey(0)
cv2.destroyAllWindows()
