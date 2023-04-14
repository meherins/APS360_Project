#imports
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import PIL.Image
import os
import shutil


folder = os.getcwd() + "/files"
if not os.path.exists(folder):
    os.makedirs(folder)


#box boundary code
def draw_bounding_box(click, x, y, flag_param, parameters):
    global x_pt, y_pt, drawing, top_left_point, bottom_right_point, original_image  
    
    if click == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_pt, y_pt = x, y   

    elif click == cv2.EVENT_MOUSEMOVE:
        if drawing:
            top_left_point, bottom_right_point = (x_pt,y_pt), (x,y)
            image[y_pt:y, x_pt:x] = 255 - original_image[y_pt:y, x_pt:x]
            cv2.rectangle(image, top_left_point, bottom_right_point, (0,255,0), 0)
    
    elif click == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left_point, bottom_right_point = (x_pt,y_pt), (x,y)
        image[y_pt:y, x_pt:x] = 255 - image[y_pt:y, x_pt:x]
        cv2.rectangle(image, top_left_point, bottom_right_point, (0,255,0), 2)
        bounding_box = (x_pt, y_pt, x-x_pt, y-y_pt)
        
        segment(original_image, bounding_box)

#grab cut
def segment(original_image, bounding_box):
    
    name = original_image
    
    x,y,width,height = bounding_box
   

    newImg = Image.fromarray(name[y:y+height, x:x+width][:, :, ::-1], 'RGB')
    rand = np.random.uniform(0,1000)
    rand2 = np.random.uniform(1,100)
    newImg.save(r'test' + str(rand) + str(rand2) + '.jpg')
    shutil.move(os.getcwd()+'\\test'+ str(rand) + str(rand2) +'.jpg', folder)

 
drawing = False
top_left_point, bottom_right_point = (-1,-1), (-1,-1)


original_image = cv2.imread("20230413_211439.JPG") #rewrite img name
original_image = cv2.resize(original_image, (750,750))
image = original_image.copy()


cv2.namedWindow('Your Ingredients')
cv2.setMouseCallback('Your Ingredients', draw_bounding_box)

while True:
    cv2.imshow('Your Ingredients', image)
    c = cv2.waitKey(1)
    if c == 27:
        break

cv2.destroyAllWindows()