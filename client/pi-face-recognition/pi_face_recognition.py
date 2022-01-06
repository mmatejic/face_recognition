# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
from PIL import Image
import requests
from numpy import asarray, array2string
import io
import base64
import json
import threading

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=False,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=False,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open("./encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

sent_request = False

def send_request(frame):
    global sent_request

    print("Sending request...")
    url = 'https://f5ef-91-208-120-1.ngrok.io/verify/'
    payload = json.dumps({'image': frame.tolist()})
    response = requests.post(url, data=payload, verify=False)
    print("Received response: " + str(response.content))
    sent_request = False

# loop over frames from the video file stream
while True:    
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(rects) and not sent_request:
        sent_request = True
        threading.Thread(target=send_request, args=(frame.copy(),)).start()
        #image = Image.fromarray(frame)
        #imgByteArr = io.BytesIO()
        #image.save(imgByteArr, format='PNG')
        #url = 'https://99c2-91-208-120-1.ngrok.io/verify/'
        #headers = {'Accept': 'text/plain'}
        #payload = json.dumps({'image': frame.tolist()})

        #response = requests.post(url, data=payload)
        #print(response)
        #image = Image.fromarray(frame)
        #imgByteArr = io.BytesIO()
        #image.save(imgByteArr, format='PNG')
        #files = {'media': imgByteArr.getvalue()}
        #files = {'media': frame.tobytes('A')}
        #response = requests.post(url, files=files)
        #print(response.content)
        
    
    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    #for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
     #   matches = face_recognition.compare_faces(data["encodings"],
       #     encoding)
      #  name = "Unknown"

        # check to see if we have found a match
       # if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
        #    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
         #   counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
          #  for i in matchedIdxs:
           #     name = data["names"][i]
            #    counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
           # name = max(counts, key=counts.get)
        
        # update the list of names
        #names.append(name)

    # loop over the recognized faces
    for (top, right, bottom, left) in boxes:
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)


    # display the image to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
