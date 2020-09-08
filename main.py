#!/usr/bin/python
import scan
import sys
import cv2
import numpy as np
import config as c


def print_coord(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)


def mean_value(image, x, y):
    pixels = 0
    mean = 0
    for i in range(x, x+15):
        for j in range(y, y+15):
            mean += image[j, i]
            pixels += 1
    return mean / pixels


def fill_shown(image, x, y):
    color = 0
    cv2.rectangle(image, (x, y), (x+14, y+14), color, -1)
    return image


def write_result(result):
    f = open("result.txt", "w")
    for i in result:
        if i == 0:
            f.write("A\n")
        else:
            f.write("F\n")


def main():
    scanned = scan.scan(sys.argv[1])
    shown = scanned
    result = []
    for column in range(0, 6):
        for group in range(0, 6):
            for i in range(0, 5):
                if len(result) == c.QUESTIONS_NUMBER:
                    break
                x_position = c.FIRST_PIXEL_X + c.COLUMN_SIZE*column
                y_position = c.FIRST_PIXEL_Y + i*c.SQUARE_SIZE + group * c.GROUP_SIZE
                mean_a = mean_value(scanned, x_position, y_position)
                mean_b = mean_value(scanned, x_position +
                                    c.A_B_OFFSET, y_position)
                if mean_a < mean_b:
                    fill_shown(shown, x_position, y_position)
                    result.append(0)
                else:
                    fill_shown(shown, x_position + c.A_B_OFFSET, y_position)
                    result.append(1)
                if c.DEBUG:
                    print(len(result), mean_a, mean_b)
    print(result)
    if c.DEBUG:
        cv2.imshow("Scanat", scanned)
        cv2.setMouseCallback("Scanat", print_coord)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
    write_result(result)


main()
