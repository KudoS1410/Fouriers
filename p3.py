"""To make a moving point on a circle image"""

import cv2 as cv
import numpy as np
import math
import colorsys as cs
import random


page = np.zeros([512, 512, 3], np.uint8)
blank = page.copy()
time = 0
yplot = []
while True:
    # reset the template each time we write a new screen
    page = blank.copy()
    # setting the drawing circle
    center = (100, 256)
    for i in range(3):

        n = 2*i +1

        radius = 50
        radius = int(4 * radius/(n * math.pi))
        # color = [0, 255, 255] # yellow
        hue = i * 360 / 200
        color = cs.hsv_to_rgb(hue, 100, 100)
        color = [int(i%255) for i in color]
        rand_col = [random.randrange(0, 255) for i in range(3)]
        # print(color)
        # color = [0, 255, 255]

        # the base circle
        cv.circle(img=page, center=center, radius = radius, color = rand_col, thickness= 4- i,lineType= cv.LINE_AA)
        # finding the point to be shown
        x = int(center[0] + radius * math.cos(n * time /20 + 0))
        y = int(center[1] + radius * math.sin(n * time /20 + 0))
        # page[y][x] = [255, 255, 255]
        # plot the point
        cv.circle(img = page, center=(x, y), radius= i % 5 + 1,color =  color,thickness = -1,lineType=cv.LINE_AA )
        center = (x, y)

    yplot.append(center[1])

    # draw the array of yplot
    ax = 255
    yplot.reverse()
    cv.line(page, center, (255, yplot[0]), [255, 255, 255], lineType=cv.LINE_AA)

    for i in range(len(yplot[:-1])):
        value = yplot[i]
        p1 = (ax, value)
        p2 = (ax+2, yplot[i+1])
        # cv.circle(page, (ax, value), 3, [255, 255, 255], -1, cv.LINE_AA)
        if ax <= 510:
            cv.line(page, p1, p2, [255, 255, 255], lineType=cv.LINE_AA)
            ax += 1
        else:
            yplot.pop(i)
    # print(len(yplot))
    yplot.reverse()

    cv.imshow('image', page)
    k = cv.waitKey(50)
    time += 1
    if k == 27:
        break
cv.destroyAllWindows()