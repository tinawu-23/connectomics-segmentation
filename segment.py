import sys
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def helpfunc():
    print('\nUsage:')
    print('python segment.py all\t\tProcess and save all images to results folder')
    print('python segment.py {imageID}\tProcess and display a specified imageID\n\n')


def process(imagefile, mode):
    # read image
    filename = 'images/' + imagefile + '.png'
    img = cv.imread(filename)

    # gray scale
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # threshold image so that it's in two colors; 
    # in this case, we're saying for all pixels > 90, set it to white
    thresh = cv.threshold(gray, 90, 255, cv.THRESH_BINARY)[1]

    # erode and dilate to get rid of noises
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=4)

    # get rid of the small spots scattered around the images
    kernel = np.ones((9, 9), np.uint8)
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    # smooths the image with median blur
    blur = cv.medianBlur(close, 3)

    # fills holes inside the images (as edges are always darker)
    final = cv.bitwise_not(blur)
    contours, hierarchy = cv.findContours(final, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv.drawContours(final, [cnt], 0, 255, -1)

    # display/save the final result with the original image
    result = np.concatenate((gray, final), axis=1)

    if mode == 'display':
        cv.imshow('result', result)
        cv.waitKey()

    elif mode == 'save':
        savefilename = 'results/' + imagefile + '.png'
        cv.imwrite(savefilename, result)



if __name__ == "__main__":

    if len(sys.argv) != 2: # input error
        helpfunc()
        exit(0)

    else:
        arg = sys.argv[1]

        # process and save all images
        if arg == 'all':
            for i in range(0,100): # image 0 to 99
                if i < 10:
                    process('00'+str(i), 'save')
                else:
                    process('0'+str(i), 'save')

        # display 1 image
        elif int(arg) >= 0 and int(arg) <= 99:
            if len(arg) == 1:
                arg = '00'+arg
            elif len(arg) == 2:
                arg = '0'+arg
            process(arg, 'display')

        # input error
        else:
            print("\nPlease enter an imageID between 0 and 99.\n")
            exit(0)
