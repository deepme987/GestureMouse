
"""
Gesture Controlled Mouse :-
===========================
GCM is a utility tool designed for presentation and distance mouse control for desktops
It makes use of hardware camera and relies on opencv and pynput for manipulating the mouse

Constants :-
============

    MOUSE_MULTIPLIER:   Movement sensitivity (ideal: 7 for 1080p)
    max_x, max_y    :   X and Y co-ordinated of display


Variables :-
============

    calibrated      :   Flag to indicate whether the movement is being captured or not
    pressed         :   Flag to indicate wrist fold

Methods :-
==========

    __main__        :   Initialize camera, generate roi_gray img of frame and call other methods
    segment         :   Search for available movement in image, return their contours, if any
    getavg          :   Balance the background at initialization
    run             :   Checks current image and modifies calibration settings or updates mouse
    calibrate       :   Turns calibrated flag to True on still hand for ~1 sec
    updatemouse     :   Finds the amount of movement and appropriately moves the mouse pointer


"""

import cv2
import imutils
from pynput.mouse import Controller, Button
import wx
import time
from win10toast import ToastNotifier

MOUSE_MULTIPLIER = 7            # Sensitivity of mouse movement

background = None               # Initial bg
app = wx.App(False)
mouse = Controller()
toaster = ToastNotifier()
max_x, max_y = wx.GetDisplaySize()      # Display Resolution

# variables used for comparision of 2 frames
old_x, old_y, old_area = 0, 0, 0
calibrated, pressed = False, False
cal_time = 0
press_time = 0


def caliberate(x, y, w, h, hull):
    global calibrated, cal_time, old_area
    time.sleep(0.1)

    if cal_time > 5:                               # If hand is still for 0.5 sec, start capturing
        print("calibrated")
        toaster.show_toast("GCM - Gesture Controlled Mouse", "calibrated", duration=0.5)

        old_area = cv2.contourArea(hull)            # Save current contour area
        calibrated = True
        mouse.position = (max_x/2 - 250, max_y/2)   # Set mouse to center of screen

    elif cal_time < 6 and x < 175 < (x+w) and y < 150 < (y+h):  # If hand is still for < 0.5 sec
        cal_time += 1
        caliberate(x, y, w, h, hull)

    return


def updateMouse(x, y, hull):
    global old_x, old_y, old_area, press_time, pressed
    time.sleep(0.2)

    area = cv2.contourArea(hull)

    if area < old_area and press_time < 15:     # Closed grip
        press_time += 1
    else:
        if 5 < press_time and area > old_area:  # Close + Open movement, MouseClickEvent
            print("Clicked")
            toaster.show_toast("GCM", "Button Clicked", duration=0.5)
            mouse.click(Button.left)
            press_time = 0

        else:                                   # Long hold, MouseGrabEven and MouseReleaseMovement
            if press_time > 100:
                if area < old_area + 2000:
                    print("Hold")
                    mouse.press(Button.left)
                    pressed = True
                elif pressed:
                    print("Release")
                    pressed = False
                    mouse.release(Button.left)
                    press_time = 0

            if x-old_x > 100 or y-old_y > 100:   # Too fast movement
                old_x, old_y = x, y
                return

            # Reset on out of boundary
            if x == 350 or x == 0:
                old_x = 0
            if y == 300 or y == 0:
                old_y = 0

            # Update mouse position
            mouse.move(MOUSE_MULTIPLIER*(x-old_x), MOUSE_MULTIPLIER*(y-old_y))
            old_x, old_y = x, y

        if press_time > 1:
            press_time -= 1


def run(hull):
    global calibrated, cal_time
    x, y, w, h = cv2.boundingRect(hull)
    # cv2.rectangle(cache, (x, y), (x+w, y+h), (255, 0, 0), 2)
    if not calibrated:                     # Check if calibration is possible
        caliberate(x, y, w, h, hull)
    elif calibrated:
        if cv2.contourArea(hull) < 3000:   # Check if un-calibration is possible
            time.sleep(0.1)
            cal_time -= 1
            if cal_time == 0:
                print("Undone")
                toaster.show_toast("GCM - Gesture Controlled Mouse", "Un calibrated", duration=0.5)
                calibrated = False
        else:                              # Update mouse position
            updateMouse(x, y, hull)
    else:                                  # No contour movements or calibration
        return


def getavg(image, aWeight):
    global background
    if background is None:
        background = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, background, aWeight)


def segment(image):
    global background
    diff = cv2.absdiff(background.astype("uint8"), image)       # Differences between current and previous state
    threshed = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    cnt, _ = cv2.findContours(threshed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnt) == 0:
        return
    else:
        seged = max(cnt, key=cv2.contourArea)
        return threshed, seged                                  # Return max contour difference


if __name__ == "__main__":
    aWeight = 0.5
    camera = cv2.VideoCapture(0)
    print("Initializing camera, smile please!")

    top, right, bottom, left = 100, 400, 400, 750       # ROI size
    num_frames = 0                                      # Frames to calibrate hull
    while True:
        _, frame = camera.read()
        frame = imutils.resize(frame, width=800)
        frame = cv2.flip(frame, 1)
        cache = frame.copy()                            # Copy of frame to use in window

        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)    # Gray image of roi
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            getavg(gray, aWeight)                       # Calibrate original background
        else:
            hand = segment(gray)

            if hand is not None:                        # If hand is detected
                threshed, seged = hand
                cv2.drawContours(cache, [seged + (right, top)], -1, (0, 255, 0))
                cv2.imshow("Threshold", threshed)

                cnt = seged.copy()
                extLeft = tuple(cnt[cnt[:, :, 0].argmin()][0])
                extRight = tuple(cnt[cnt[:, :, 0].argmax()][0])
                extTop = tuple(cnt[cnt[:, :, 1].argmin()][0])
                extBot = tuple(cnt[cnt[:, :, 1].argmax()][0])
                hull = ()

                if cv2.contourArea(cnt) > 3000:         # Hand area to compare closed and opened fist
                    hull = cv2.convexHull(cnt)
                run(cnt)

                if hull != ():
                    cv2.drawContours(cache, [hull + (right, top)], -1, (0, 0, 255), 2)

        cv2.rectangle(cache, (left, top), (right, bottom), (0, 255, 0), 2)        # ROI Rectangle in window frame
        num_frames += 1
        cv2.imshow("Input", cache)

        keypress = cv2.waitKey(1) & 0xFF
        if keypress == 27:                               # Exit on "Esc"
            break

    # Free up resources on exit
    camera.release()
    cv2.destroyAllWindows()

