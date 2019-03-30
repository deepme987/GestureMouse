import cv2
import imutils
import numpy as np
from pynput.mouse import Controller, Button
import wx
import time
from win10toast import ToastNotifier

background = None
app = wx.App(False)
mouse = Controller()
toaster = ToastNotifier()
max_x, max_y = wx.GetDisplaySize()
# mouse.position = (100, 100)

old_x, old_y, old_area = 0, 0, 0
caliberated, pressed = 0, 0
cal_time = 0
press_time = 0


def caliberate(x, y, w, h, hull):
    global caliberated, cal_time, old_area
    time.sleep(0.1)

    if cal_time != 0:
        print(cal_time)

    if cal_time > 5:
        print("Caliberated")
        toaster.show_toast("GCM - Gesture Controlled Mouse", "Caliberated", duration=0.5)

        old_area = cv2.contourArea(hull)
        caliberated = 1
        print(max_x, max_y)
        mouse.position = (max_x/2 - 250, max_y/2)

    elif cal_time < 6 and x < 175 < (x+w) and y < 150 < (y+h):
        cal_time += 1
        caliberate(x, y, w, h, hull)

    return


def updateMouse(x, y, hull):
    global old_x, old_y, old_area, press_time, pressed
    time.sleep(0.3)

    area = cv2.contourArea(hull)
    print(area, press_time)

    if area < old_area and press_time < 15:
        press_time += 1
    else:
        if 5 < press_time and area > old_area:
            print("Clicked")
            toaster.show_toast("GCM", "Button Clicked", duration=0.5)
            mouse.click(Button.left)
            press_time = 0

        else:
            if press_time > 100:
                if area < old_area + 2000:
                    print("Hold")
                    mouse.press(Button.left)
                    pressed = 1
                elif pressed == 1:
                    print("Release")
                    pressed = 0
                    mouse.release(Button.left)
                    press_time = 0
            if x-old_x > 100 or y-old_y > 100:
                old_x, old_y = x, y
                return

            if x == 350 or x == 0:
                old_x = 0
            if y == 300 or y == 0:
                old_y = 0
            mouse.move(7*(x-old_x), 7*(y-old_y))
            old_x, old_y = x, y
        if press_time > 1:
            press_time -= 1


def counts(hull):
    global caliberated, cal_time
    x, y, w, h = cv2.boundingRect(hull)
    cv2.rectangle(cache, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # print(x, y, w, h)
    if caliberated == 0:
        caliberate(x, y, w, h, hull)
    elif caliberated == 1 and cv2.contourArea(hull) < 3000:
        time.sleep(0.1)
        cal_time -= 1
        if cal_time > 0:
            print(cal_time)
        if cal_time == 0:
            print("Undone")
            toaster.show_toast("GCM - Gesture Controlled Mouse", "Un caliberated", duration=0.5)
            caliberated = 0
    elif caliberated == 1:
        updateMouse(x, y, hull)
    else:
        return


def getAvg(image, aWeight):
    global background
    if background is None:
        background = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, background, aWeight)


def segment(image):
    global background
    diff = cv2.absdiff(background.astype("uint8"), image)
    threshed = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    cnt, _ = cv2.findContours(threshed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnt) == 0:
        return
    else:
        seged = max(cnt, key=cv2.contourArea)
        return threshed, seged


if __name__ == "__main__":
    aWeight = 0.5
    camera = cv2.VideoCapture(0)

    top, right, bottom, left = 100, 400, 400, 750
    num_frames = 0
    x = 0
    while True:
        _, frame = camera.read()
        frame = imutils.resize(frame, width=800)
        frame = cv2.flip(frame, 1)
        cache = frame.copy()

        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            getAvg(gray, aWeight)
        else:
            hand = segment(gray)

            if hand is not None:
                threshed, seged = hand
                cv2.drawContours(cache, [seged + (right, top)], -1, (0, 255, 0))
                cv2.imshow("Threshold", threshed)
                # print(threshed)
                # cv2.imshow("a", seged)

                cnt = seged.copy()
                extLeft = tuple(cnt[cnt[:, :, 0].argmin()][0])
                extRight = tuple(cnt[cnt[:, :, 0].argmax()][0])
                extTop = tuple(cnt[cnt[:, :, 1].argmin()][0])
                extBot = tuple(cnt[cnt[:, :, 1].argmax()][0])
                hull = ()

                if cv2.contourArea(cnt) > 3000:
                    hull = cv2.convexHull(cnt)
                counts(cnt)

                if hull != ():
                    cv2.drawContours(cache, [hull + (right, top)], -1, (0, 0, 255), 2)
        cv2.rectangle(cache, (left, top), (right, bottom), (0, 255, 0), 2)
        num_frames += 1
        cv2.imshow("Input", cache)
        keypress = cv2.waitKey(1) & 0xFF

        if keypress == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

