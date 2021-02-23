import cv2, time, pandas
from datetime import datetime
import imutils

first_frame = None
status_list = [None, None]  # to prevent index out of bound error at the beginning
times = []
df = pandas.DataFrame(columns=["Start", "End"])

# video = cv2.VideoCapture(cv2.CAP_DSHOW)
f = "e:\\DEV\\MSVC_Projects\\Astronomy\\test.mp4"
video = cv2.VideoCapture(f)

time.sleep(2)
is_video = True
vs = video
firstFrame = None
frame_num = 0
dx = 127
dy = 255
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if not is_video else frame[1]

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=700)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, dx, dy, cv2.THRESH_BINARY)[1]
    firstFrame = gray

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        # if cv2.contourArea(c) < args["min_area"]:
        t = cv2.contourArea(c)
        if t < 1:
            continue
        if t > 200:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(frame, "frame {}".format(frame_num), (0, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "DX={0} DY={1}".format(dx, dy), (0, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.moveWindow("Security Feed", 0, 0)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.moveWindow("Frame Delta", 0, 400)
    cv2.imshow("Thresh", thresh)
    cv2.moveWindow("Thresh", 0, 800)
    key = cv2.waitKeyEx(1)

    if key in [0x1b, ord('q')]:
        break
    if key == 0x250000:  # left
        frame_num -= 30
        if (frame_num < 0):
            frame_num = 0
        print("rewind")
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    if key == 0x260000:  # up
        dx += 1
        if (dx > 255):
            dx = 255
    if key == 0x280000:  # down
        dx -= 1
        if (dx < 0):
            dx = 0
    if key == 0x2d:  # -
        dy -= 10
        if (dy < 0):
            dy = 0
    if key == 0x2b:  # +
        dy += 10
        if (dy > 255):
            dy = 255
        pass
    if key >= 0:
        print(hex(key))

    frame_num += 1
    if(frame_num>300):
        frame_num=0
        print("rewind")
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

print(status_list)
print(times)

video.release()
cv2.destroyAllWindows()
