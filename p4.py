"""To make a moving point on a circle image"""

import cv2 as cv
import numpy as np
import math
import colorsys as cs
import random


def dft(values, detail):
    total = len(values)
    c = (2 * math.pi) / total
    amplitude = [0 for i in range(detail)]
    frequency = [0 for i in range(detail)]
    phase = [0 for i in range(detail)]
    for i in range(detail):
        sum_real = 0
        sum_img = 0
        k = i
        for n in range(total):
            sum_real += values[n] * math.cos(n * k)
            sum_img -= values[n] * math.sin(n * k)
        # having done the summation we are done with integration almost
        coeff = [sum_real * c, sum_img * c]
        # amplitude = mod(coeff)
        amplitude[i] = math.sqrt(coeff[0] * coeff[0] + coeff[1] * coeff[1])
        # frequency = k/2pi
        frequency[i] = k / (2 * math.pi)
        # phase is phase of complex number coeff
        phase[i] = math.atan2(sum_real, sum_img)

    return amplitude, phase, frequency



page = np.zeros([600,1000, 3], np.uint8)
w = 1000
h = 600
blank = page.copy()
time = 0
yplot = []
# pattern = []

pattern = [10 * math.sin(i / (180/math.pi)) for i in range(1000)]
pattern = [math.tan(i) for i in range(0, 1000)]
# pattern = [random.randrange(-50, 50) for i in range(1000)]
# pattern = [10 *math.cos(i) for i in range(100)]
# pattern = []
amplitude, phases, frequency =dft(pattern, 50)
print(pattern)
print(amplitude)
print(phases)
print(frequency)
l = len(amplitude)

# drawing the given sampling

constant = 2 * math.pi / (l * 1)
while True:
    # reset the template each time we write a new screen
    center = (256, 256)
    page = blank.copy()
    # setting the drawing circle
    for i in range(0, l):


        radius = int(1 * amplitude[i])
        freq = frequency[i]
        phase = phases[i]

        hue = i * 360 / 200
        color = cs.hsv_to_rgb(hue, 100, 100)
        color = [int(i%255) for i in color]
        rand_col = [random.randrange(0, 255) for i in range(3)]


        # the base circle
        cv.circle(img=page, center=center, radius = radius, color = rand_col, thickness= 1,lineType= cv.LINE_AA)


        # finding the point to be shown
        x = int(center[0] + radius * math.cos(freq * time + phase))
        y = int(center[1] + radius * math.sin(freq * time + phase))
        # page[y][x] = [255, 255, 255]
        # plot the point
        cv.circle(img = page, center=(x, y), radius= i % 5 + 1,color =  color,thickness = -1,lineType=cv.LINE_AA )
        center = (x, y)

    yplot.append(center[1])

    # draw the array of yplot
    ax = 500
    yplot.reverse()
    cv.line(page, center, (ax, yplot[0]), [255, 255, 255], lineType=cv.LINE_AA)

    for i in range(len(yplot[:-1])):
        value = yplot[i]
        p1 = (ax, value)
        p2 = (ax+2, yplot[i+1])
        # cv.circle(page, (ax, value), 3, [255, 255, 255], -1, cv.LINE_AA)
        if ax <= w-2:
            cv.line(page, p1, p2, [255, 255, 255], lineType=cv.LINE_AA)
            ax += 1
        else:
            yplot.pop(i)
    # print(len(yplot))
    yplot.reverse()

    cv.imshow('image', page)
    k = cv.waitKey(1)
    time += constant
    if k == 27:
        break
cv.destroyAllWindows()