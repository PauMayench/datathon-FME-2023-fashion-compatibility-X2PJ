from obtenirDades import obtenirDades
from mixImage import  cropClassifyImages
from pprint import pprint
import cv2

#id = 431 #
id = 497

i = 0
outfits = obtenirDades()

o = outfits[id]
cropped_classified_images = cropClassifyImages(o)


pprint(cropped_classified_images.items())




'''
for outfit in outfits.values():
    cropped_classified_images = cropClassifyImages(outfit)
    imatgeFinal = mixImage(cropped_classified_images)
    i += 1
    cv2.imshow('Mix Image', imatgeFinal)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if i > 3: break'''


#imatgeFinal = mixImage(cropped_classified_images)
#i += 1
#cv2.imshow('Mix Image', imatgeFinal)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
