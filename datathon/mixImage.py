import cv2
import numpy as np

#['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops', 'Accesories, Swim and Intimate', 'Outerwear', 'Beauty', 'Home']

# li dones un outfuit (llista de prendas)
def cropClassifyImages(prendas):
    cropped_classified_images = {}
    for prenda in prendas.values():
        image = cv2.imread(prenda.des_filename)
        if image is None:
            print(f"Image not found: {prenda.des_filename}")
            continue
        

        noResize = ['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops']
        if True or (prenda.des_product_category in noResize):
            if(prenda.des_product_category in cropped_classified_images):
                cropped_classified_images[prenda.des_product_category].append(image)
            else:
                cropped_classified_images[prenda.des_product_category] = [image]
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, threshold1=50, threshold2=100)

        pts = np.argwhere(edges > 0)
        
        if pts.size > 0:
            top_left = pts.min(axis=0)
            bottom_right = pts.max(axis=0)

            padding = 10
            start_x, start_y = max(0, top_left[1] - padding), max(0, top_left[0] - padding)
            end_x, end_y = min(image.shape[1], bottom_right[1] + padding), min(image.shape[0], bottom_right[0] + padding)

            cropped_image = image[start_y:end_y, start_x:end_x]

            #cv2.imshow('Original Image', image)
            #cv2.imshow('Cropped Image', cropped_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            if(prenda.des_product_category in cropped_classified_images):
                cropped_classified_images[prenda.des_product_category].append(cropped_image)
            else:
                cropped_classified_images[prenda.des_product_category] = [cropped_image]
        else:
            print(f"No edges detected in image: {prenda.des_filename}")
            image = cv2.imread(prenda.des_filename)
            if image is None:
                print(f"Image not found: {prenda.des_filename}")
                cropped_classified_images[prenda.des_product_category] = image
    return cropped_classified_images


def mixImage(cropped_classified_images):
    # Define canvas size
    canvas_width, canvas_height = 239*5, 334*3
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    # Define regions for each category
    #['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops', 'Accesories, Swim and Intimate', 'Outerwear', 'Beauty', 'Home']

    regions = { #home and beauty where deemed irrelevant to try to improve the performance of the training 
        "Tops": 0,
        "Dresses, jumpsuits and Complete set":3,
        "Bottoms": 5,
        "Accesories, Swim and Intimate":10,
        "Outerwear": 8
    }

    x_img = 239
    y_img = 334

    for category, image_list in cropped_classified_images.items():
        if category in regions:
            # Determine region size
            #region_height, region_width = region[0].stop - region[0].start, region[1].stop - region[1].start

            #region_image = np.zeros((region_height, region_width, 3), dtype=np.uint8)
            #current_x = 0  # Start position for the first image
            try:
                count = regions[category]
                for image in image_list:
                    if count >= 15: count = 8
                    canvas[0+int(count/5)*y_img:y_img+int(count/5)*y_img, count%5*x_img:x_img+count%5*x_img] = image
                    count += 1
            except:
                pass

    return canvas
