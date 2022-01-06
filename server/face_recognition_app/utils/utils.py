import numpy
from imutils import paths
import face_recognition
import pickle
import cv2
import os
from django.conf import settings
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_single_face(image):
    image = Image.open(image.file)
    array = numpy.array(image)
    encodings = check_faces(array)

    if not encodings:
        raise ValidationError("Image must contain at least one face")
    elif len(encodings) > 1:
        raise ValidationError("Image must not contain more than one face")

def check_faces(array):
    detector = cv2.CascadeClassifier(
        os.path.join(settings.BASE_DIR, "face_recognition_app/utils/haarcascade_frontalface_default.xml")
    )

    gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    return face_recognition.face_encodings(rgb, boxes)


def encode_faces():
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(os.path.join(settings.BASE_DIR, "static/images")))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        folderName = imagePath.split(os.path.sep)[-2].split("_")
        name = f"{folderName[1]} {folderName[2]}"
        print(name)
        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}

    f = open(os.path.join(settings.BASE_DIR, "encodings.pickle"), "wb")
    f.write(pickle.dumps(data))
    f.close()
