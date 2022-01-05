import base64
import io
import json
import pickle
from io import BytesIO

import cv2
import face_recognition
from PIL import Image, ImageOps
from django.http import HttpResponse, FileResponse
import numpy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.parsers import BaseParser
from rest_framework.decorators import parser_classes

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


@parser_classes([PlainTextParser])
class Verify(APIView):
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(
        open(r"C:\code\master\face_recognition_project\pi-face-recognition\encodings.pickle", "rb").read())
    detector = cv2.CascadeClassifier(
        r"C:\code\master\face_recognition_project\pi-face-recognition\haarcascade_frontalface_default.xml")

    def post(self, request, format=None):
        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        str = json.loads(request.data)['image']
        # bytes = base64.b64decode(image_base64.encode('utf-8'))
        arr = numpy.array(str, dtype=numpy.uint8)

        image = Image.fromarray(arr)

        image.show()
        # convert image to numpy array
        array = numpy.array(image)
        gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"],
                                                     encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
                # update the list of names
            names.append(name)

        return Response(names)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(array, (left, top), (right, bottom),
                          (117, 33, 143), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(array, name, (left, y), cv2.FONT_HERSHEY_PLAIN,
                        1.25, (117, 33, 143), 2)

        img = Image.fromarray(array, 'RGB')

        response = HttpResponse(content_type='image/jpg')
        img.save(response, "JPEG")
        return response

        return FileResponse(img)
