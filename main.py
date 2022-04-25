from asyncio import threads
import cv2
import numpy as np
#from utils import biggestContour, drawRectangle, reorder, valTrackbars
#Utility functions for document scanner
##############################
#trackbar code
def nothing(x):
    pass

########################################################
webCamFeed = False
pathImage = "Images\\images004.jpg"
cap = cv2.VideoCapture(0)
cap.set(10,160)
heightImg = 640
widthImg = 480
#####################################################


# function to initialize Trackbars
def initializeTrackbars(intialTracbarVal=125):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", intialTracbarVal,255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", intialTracbarVal, 255, nothing)
def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Threshold1,Threshold2
    return src

#find biggest countour
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    #loop through countours list
    for i in contours:
        area = cv2.contourArea(i)
        #discard areas below treshold
        if area > 5000:
            #calculates a contour perimeter -> float
            peri = cv2.arcLength(i, True)
            #calcualtes a curve or a polygon with another curve/polygon with less vertices
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print(f'Area: {area}, Peri: {peri}, Approx: {approx}')
            # is it a rectangle?
            if area > max_area and len(approx) == 4:
                biggest = approx
                #overwrite max_area for regions that are lareger
                max_area = area
    return biggest,max_area
 
#reordering points in order to warp image
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
 
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    
    return myPointsNew   
 
def drawRectangle(img,biggest,thickness):
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 155, 0), thickness)
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 155, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 155, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 155, 0), thickness)
 
    return img

initializeTrackbars (125)
count=0
#imgBlank = 
while True:
    #input is either webcam or image
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(pathImage)



    #start the pipline of the project
    img = cv2.resize(img, (widthImg, heightImg))   #RESIZE IMAGE

    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) #CREATE A BLANK IMAGE FOR 
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #COVERT IMG TO GRAY SCALE 
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) #ADD GAUSSIAN BLUR
    thres=valTrackbars() #get track bar vaalues for thresholds
    imgCanny = cv2.Canny(imgBlur,thres[0],thres[1])#apply canny blur
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2) #APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1 ) #APPLY EROSION
    imgContours =img.copy()
    imgFinal = imgCanny

    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgThreshold, contours, -1,(0,255,0), 10) # draw contours
    biggest, area=biggestContour(contours) # biggest contours
    newpoints=reorder(biggest) # reoreder points
    #drawrec=drawRectangle()


    pts1 = np.float32(newpoints)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))





    cv2.imshow("1. Original", img)
    cv2.imshow("2. Grayscale", imgGray)
    cv2.imshow("3. Blur", imgBlur)
    cv2.imshow("4. Canny", imgCanny)
    cv2.imshow("5. Dilate", imgDial)
    cv2.imshow("6. Treshold", imgThreshold)
    cv2.imshow("7. imgContours", imgContours)
    cv2.imshow("8. imgWarpColored", imgWarpColored)

    #Press x on keybord to exit
    #Close and break the loop after pressing "X" key
    if cv2.waitKey(1) & 0XFF == ord('x'):
        break # exit infinite loop

    #save image when 's' key is pressed
    if cv2.waitKey(1) & 0XFF == ord('s'):
        print("saving")
        cv2.imwrite("Scanned/myIamge"+str(count)+".jpg", imgFinal)
        cv2.waitKey(300)
        count +=1
            
#when everything done release
# the video capture object
cap.release()            

#closes all the frames 
cv2.destroyAllWindows()
