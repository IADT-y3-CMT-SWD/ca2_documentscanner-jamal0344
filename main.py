import cv2
import numpy as np
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


initializeTrackbars (125)
count=0
imgBlank = 
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
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2) #APPLY DILATION
    imgthreshold = cv2.erode(imgDial, kernel, iterations=1 ) #APPLY EROSION


    cv2.imshow("1. Original", img)
    cv2.imshow("2. Grayscale", imgGray)
    cv2.imshow("3. Blur", imgBlur)
    cv2.imshow("4. Canny", imgCanny)
    cv2.imshow("5. Dilate", imgDial)
    cv2.imshow("6. Treshold", imgthreshold)
    cv2.imshow("7. imgContours", imgContours)

    #Press x on keybord to exit
    #Close and break the loop after pressing "X" key
    if cv2.waitKey(1) & 0XFF == ord('x'):
        break # exit infinite loop

    #save image when 's' key is pressed
    if cv2.waitKey(1) & 0XFF == ord('s'):
        print("saving")
        cv2.imwrite("Scanned/myIamge"+str(count)+".jpg", imgContours)
        cv2.waitKey(300)
        count +=1
            
#when everything done release
# the video capture object
cap.release()            

#closes all the frames 
cv2.destroyAllWindows()
