"""To make a moving point on a circle image
and plot its yaxis value"""

import cv2 as cv
import numpy as np
import math


page = np.zeros([512, 512, 3], np.uint8)
blank = page.copy()
time = 0
yplot = []
while True:
    page = blank.copy()
    # setting the drawing circle parameters
    center = (100, 256)
    radius = 50
    color = [0, 255, 255]
    # drawing the base circle
    cv.circle(img=page, center=center, radius = radius, color = color, thickness=1,lineType= cv.LINE_AA)
    x = int(center[0] + radius * math.cos(time/40))
    y = int(center[1] + radius * math.sin(time/40))
    yplot.append(y)
    # drawing the point
    # page[y][x] = [255, 255, 255]
    cv.circle(img = page, center=(x, y), radius=5,color =  [255, 255, 255],thickness = -1,lineType=cv.LINE_AA )

    
    ax = 255
    yplot.reverse()
    # first join the last plotted point with the plotting point of the curve
    cv.line(page, (x, y), (255, yplot[0]), [255, 255, 255], lineType=cv.LINE_AA)

    # draw the array of yplot
    for i in range(len(yplot[:-1])):
        value = yplot[i]
        p1 = (ax, value)
        p2 = (ax+2, yplot[i+1])
        # joining succesive points
        if ax <= 510:
            cv.line(page, p1, p2, [255, 255, 255], lineType=cv.LINE_AA)
            ax += 1
        else:
            yplot.pop(i)
    print(len(yplot))
    yplot.reverse()

    cv.imshow('image', page)
    k = cv.waitKey(1)
    time += 1
    # setting the exit key to esc key
    if k == 27:
        break
