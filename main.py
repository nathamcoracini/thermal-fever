import cv2
import sys
import pandas as pd

# Algorithm to detect faces
def detect_face(imgrgb, filename):

    # Resize image to fit screen
    imgrgb = cv2.resize(imgrgb, (820, 616))

    # Flip image to match thermal
    imgrgb = cv2.flip(imgrgb, 1)

    # Array for cropped face
    face_crop = []

    # Convert to grayscale
    gray = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(imgrgb, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_crop.append(imgrgb[y:y+h, x:x+w])
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = imgrgb[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    title = "Face " + str(filename);

    cv2.imshow(title, face_crop[0])
    # cv2.imshow('rgb', imgrgb)

def detect_temperature(img, filename, csvname):


    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    pos = (10, 30)
    pos2 = (10, 60)

    # fontScale
    fontScale = 0.5

    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 1

    # open CSV
    df=pd.read_csv(csvname, sep=';')

    # Get Max Value
    column_maxes_series = df.max()
    maxtmp = column_maxes_series.max()

    finaltmp = float(maxtmp)

    if (finaltmp > 37.5):
        img = cv2.putText(img, 'Febre: Sim', pos2, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        img = cv2.putText(img, 'Febre: Nao', pos2, font, fontScale, color, thickness, cv2.LINE_AA)

    img = cv2.putText(img, 'Temperatura: ' + str(finaltmp), pos, font,
                   fontScale, color, thickness, cv2.LINE_AA)


    title = "Thermal image " + str(filename);

    cv2.imshow(title, img)

imglist = []
imglistrgb = []
count = 0

# Read images from command line
for arg in sys.argv:
    if (arg != "main.py"):
        if (count % 2 == 0):
            imglist.append(arg)
        else:
            imglistrgb.append(arg)
        count = count + 1

# Load the cascade
face_cascade = cv2.CascadeClassifier('face_cascade.xml')
eye_cascade = cv2.CascadeClassifier('eye_cascade.xml')

# Load images to detect
for image in imglist:
    img = cv2.imread(image)
    csvname = image
    csvname = csvname[:-4]
    finalcsv = csvname + ".csv"
    detect_temperature(img, image, finalcsv)

for image in imglistrgb:
    imgrgb = cv2.imread(image)
    detect_face(imgrgb, image)

cv2.waitKey(0);

cv2.destroyAllWindows();
