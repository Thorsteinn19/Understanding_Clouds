import cv2
import numpy as np
from PIL import Image
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import pandas as pd
import csv

def rle_decode(mask_rle, shape=(2100, 1400)):
    '''
    mask_rle: run-length as string formated (start length)
    shape: (height,width) of array to return 
    Returns numpy array, 1 - mask, 0 - background
    '''
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape).T  # Needed to align to RLE direction

def masks_as_image(in_mask_list, all_masks=None):
    # Take the individual ship masks and create a single mask array for all ships
    if all_masks is None:
        all_masks = np.zeros((1400, 2100), dtype = np.int8)
    #if isinstance(in_mask_list, list):
    for mask in in_mask_list:
        if isinstance(mask, str):
            all_masks += rle_decode(mask)
    return all_masks

masks = pd.read_csv('train.csv')
imagelabels = masks['Image_Label']

with open('trainbb2.csv','w',newline='\n') as csv_file:
    fieldnames = ['imagelabel', 'h', 'w', 'y', 'x']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for imagelabel in imagelabels:
        rle_0 = masks.query('Image_Label=="'+imagelabel+'"')['EncodedPixels']
        boxlist=[]
        mask_0 = masks_as_image(rle_0)
        print(np.max(mask_0))
        lbl_0 = label(mask_0) 
        print(np.unique(lbl_0))
        for color in np.unique(lbl_0)[1:]:
            x, y, w, h = cv2.boundingRect(np.uint8(lbl_0 == color))
            #print('Found bbox', x, y, w, h)
            if (w**2+h**2)**0.5 > 100:
                writer.writerow({'imagelabel': imagelabel, 'h': h, 'w':w, 'y':y, 'x': x})
    #Need to add here the code to save the boxes to a csv file

#        cv2.rectangle(img_1, (x, y), (x+w, y+h), (0, 0, 255), 2)

#fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (15, 5))
#ax1.imshow(img)
#ax1.set_title('Image')
#ax2.set_title('Mask')
#ax3.set_title('Image with derived bounding box')
#ax2.imshow(lbl_0)
#ax3.imshow(img_1)
#plt.show()
#cv2.waitKey(0)
#cv2.destroyAllWindows()