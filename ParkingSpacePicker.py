import cvzone
import cv2 as cv
import pickle

img = cv.imread('/Users/nanda/PycharmProjects/Parking Space Counter/Resources/CarParkProject/carParkImg.png')

try:
    with open(('CarParkPos'), 'rb') as f:
        posList = pickle.load(f) ## if there is a previous box in the image we are going to load the old value instead of new list
except:
    posList = [] ## if theres no old list we will create new list
width , height = 107,48

def mouseClick(events,x,y,flags,params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events==cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open(('CarParkPos'),'wb') as f:
        pickle.dump(posList,f)



while True:
    img = cv.imread('/Users/nanda/PycharmProjects/Parking Space Counter/Resources/CarParkProject/carParkImg.png')
    for pos in posList:
        cv.rectangle(img,pos,(pos[0]+width,pos[1]+height),(0,255,0),2)
    # cv.rectangle(img,(50,192),(155,242),(255,0,255),2)
    #Detect Moouse Click


    cv.imshow('Image',img)
    cv.setMouseCallback('Image',mouseClick)

    cv.waitKey(1)