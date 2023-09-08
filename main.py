import cv2 as cv
import pickle
import cvzone
import numpy
import numpy as np

##Video feed
width , height = 107,48
cap = cv.VideoCapture('/Users/nanda/PycharmProjects/Parking Space Counter/Resources/CarParkProject/carPark.mp4')

with open(('CarParkPos'), 'rb') as f:
    posList = pickle.load(f)  ## if there is a previous box in the image we are going to load the old value instead of new list


def checkParkingSpace(imgProc):
    spaceCounter = 0
    for pos in posList:
        x,y = pos


        imgCrop = imgProc[y:y+height,x:x+width]
        cv.imshow(str(x*y),imgCrop)
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3),1,1,offset=0,colorR=(0,0,255))


        if count <890 :
            color = (0,255,0)
            thickness = 5
            cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), 1, 1, offset=0, colorR=color)
            spaceCounter+= 1
        else:
            color = (0,0,255)
            thickness = 2
            cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color,thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), 1, 1, offset=0, colorR=color,colorB=(0,0,0))

    cv.putText(img,f'Free : {spaceCounter}/{len(posList)}', (80,40),1,2,(0,255,0),thickness=3)


while True:

    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT): ## if current frames equals to the total frames
        cap.set(cv.CAP_PROP_POS_FRAMES,0) ## We are going to reppeat the video by settinf the value to 0

    success,img = cap.read()

    ## Thresholding

    imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv.adaptiveThreshold(imgBlur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv.THRESH_BINARY_INV,25,16)
    imgMedian = cv.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)

    imgDilate = cv.dilate(imgMedian,kernel,iterations=1)


    checkParkingSpace(imgDilate)

    # for pos in posList:



    cv.imshow('Image',img)
    # cv.imshow('Image blur', imgBlur)
    # cv.imshow('Image Thresh', imgThreshold)
    # cv.imshow('Image Median', imgMedian)
    # cv.imshow('Image Dilate', imgDilate)

    cv.waitKey((1))