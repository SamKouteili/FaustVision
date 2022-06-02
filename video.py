from time import sleep
import numpy as np
import cv2 as cv
from pythonosc.udp_client import SimpleUDPClient

# CONSTS
LARGE_MOVEMENT = 40000


def address(col, t) :
    if t == 'f' :
        return f'/main/{col}Freq'
    if t == 'g' :
        return f'/main/{col}Gain'

def printMsg(add, mes) :
    print(f'MESSAGE {mes} SENTTO: {add}')
    return

def getThreshDict() :
    
    d = {}
    f = open("thresh.txt", "r")
    for l in f :
        l = l[:-1]
        kv = l.split("=")
        rg = kv[1].split("-")
        d[kv[0]] = [int(rg[0]), int(rg[1])]
    
    return d

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

re, initial_frame = cap.read()

SIZE = initial_frame.shape
THRESH = getThreshDict()

# background substitution for motion detection
backSub = cv.createBackgroundSubtractorMOG2(history=100, detectShadows=True, varThreshold=128)

client = SimpleUDPClient("localhost", 5510)

def normalize(i, ax, col) :
    yr, xr, _ = SIZE
    std = xr if ax == 'x' else yr
    mu = THRESH[col] if ax == 'x' and col in THRESH  else [0, 1]
    return i*(mu[1] - mu[0])/std

# convenience function to color-threshold any frame
def send_color_message(frame, hsv_frame, col, lower_thresh, upper_thresh, rec_color):
    mask = cv.inRange(hsv_frame, lower_thresh, upper_thresh)
    cnts, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    addf = address(col, 'f')
    addg = address(col, 'g')

    found_valid_cnt = False
    for (i, c) in enumerate(cnts):
        size = cv.contourArea(c)
        
        if size < 500 or hierarchy[0][i][3] != -1:
            continue
        
        found_valid_cnt = True
        m = cv.moments(c)

        cnt_x = int(m['m10']/m['m00'])
        cnt_y = int(m['m01']/m['m00'])

        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), rec_color, 2)

        client.send_message(addf, normalize(cnt_x, 'x', col))
        client.send_message(addg, normalize(cnt_y, 'y', col))
        # printMsg(addf, cnt_x)
        # printMsg(addg, cnt_y)

    if not found_valid_cnt:

        client.send_message(addf, 0)
        client.send_message(addg, 0)
        # printMsg(addf, 0)
        # printMsg(addg, 0)


frame_num = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame = cv.flip(frame, 1)
    fgMask = backSub.apply(frame)
    fgMask = cv.GaussianBlur(fgMask, (5, 5), 0)
    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # DETECT COLOR OBJECTS
    if frame_num % 5 == 0:
        send_color_message(frame, hsvFrame, "blue", np.array([91,60,38]), np.array([112,236,222]), rec_color=(255, 0, 0))
        send_color_message(frame, hsvFrame, "red", np.array([167,117,96]), np.array([179,225,219]), rec_color=(0, 0, 255))

    if frame_num % 8 == 0:
        send_color_message(frame, hsvFrame, "green", np.array([37, 24, 21]), np.array([82, 99, 171]), rec_color=(0, 255, 0))
        send_color_message(frame, hsvFrame, "yellow", np.array([12, 59, 99]), np.array([62, 133, 232]), rec_color=(128, 241, 236))    

    # osc_process()

    # CALCULATE MOVEMENT (send average of top 5)
    cnts, hierarchy = cv.findContours(fgMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cnts_avg_x = 0
    cnts_avg_y = 0
    valid_cnts = 0
    large_mvmt_found = False
    large_mvmt_size = 0
    for (i, c) in enumerate(cnts):
        size = cv.contourArea(c)

        if size < 800  or hierarchy[0][i][3] != -1:
            continue
        
        if size > LARGE_MOVEMENT and size > large_mvmt_size:
            large_mvmt_found = True
            large_mvmt_size = size

        m = cv.moments(c)

        cnts_avg_x += int(m['m10']/m['m00'])
        cnts_avg_y += int(m['m01']/m['m00'])
        valid_cnts += 1

        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), (242, 131, 159), 2)


    cv.imshow('Frame', frame)

    # send all OSC messages at the end of each frame process loop
    # osc_process()
    frame_num += 1
    if cv.waitKey(10) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

# msg = oscbuildparse.OSCMessage("/final", None, [1])
# osc_send(msg, "faust")
sleep(1)


# osc_process()
# osc_terminate()
