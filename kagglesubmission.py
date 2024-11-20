import pandas as pd
import csv

masks = pd.read_csv('sample_submission.csv')
submission=pd.read_csv('results.csv')
imagelabels = masks['Image_Label']


outdictionary = {}
for A in imagelabels:
    key=str(A)
    values=submission.query('Image_Label=="'+key+'"')['EncodedPixels']
    for value in values:
        if type(value)==str:
            outdictionary[key] = value
        else:
            outdictionary[key] = ''
    if values.shape[0]==0:
        outdictionary[key] = ''

with open('submission.csv', 'w',newline='\n') as csvfile: 
    fieldnames = ['Image_Label','EncodedPixels']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

    writer.writeheader() 
    for key2 in outdictionary:
        printkey=key2
        printvalue=outdictionary[key2]
        writer.writerow({'Image_Label': printkey, 'EncodedPixels': printvalue}) 

#for image in imagelabels:


