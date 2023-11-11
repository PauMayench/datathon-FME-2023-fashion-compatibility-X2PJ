import cv2
import numpy as np

#['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops', 'Accesories, Swim and Intimate', 'Outerwear', 'Beauty', 'Home']

# li dones un outfuit (llista de prendas)
def cropClassifyImages(outfit):
    cropped_classified_images = {}
    for prenda in outfit.prendas.values():
        image = cv2.imread(prenda.des_filename)
        if image is None:
            print(f"Image not found: {prenda.des_filename}")
            continue
        

        noResize = ['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops']
        #if prenda.des_product_category in noResize:
        #    cropped_classified_images[prenda.des_product_category] = image
        #    continue

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

'''
def mixImage(cropped_classified_images):
    # Define canvas size
    canvas_width, canvas_height = 800, 600
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8)

    # Define regions for each category
    regions = {
        "Bottoms": (slice(100, 450), slice(200, 600)),
        "Tops": (slice(150, 300), slice(200, 600)),
        "Dresses, jumpsuits and Complete set": (slice(0, 150), slice(0, canvas_width)),
        "Accesories, Swim and Intimate": (slice(450, 500), slice(0, canvas_width)),
        "Outerwear": (slice(500, 550), slice(0, canvas_width)),
        "Beauty": (slice(550, 575), slice(0, canvas_width)),
        "Home": (slice(575, 600), slice(0, canvas_width)),
    }

    for category, image_list in cropped_classified_images.items():
        if category in regions:
            # Determine region size
            region = regions[category]
            region_height, region_width = region[0].stop - region[0].start, region[1].stop - region[1].start

            region_image = np.zeros((region_height, region_width, 3), dtype=np.uint8)
            current_x = 0  # Start position for the first image
            
            for image in image_list:
                # Calculate the aspect ratio of the original image
                h, w = image.shape[:2]
                aspect_ratio = w / h

                # Determine new height and width to maintain aspect ratio
                new_width = int(aspect_ratio * region_height)
                new_height = region_height

                # If the width exceeds the region's width, adjust it
                if new_width > region_width:
                    new_width = region_width
                    new_height = int(region_width / aspect_ratio)

                # Resize image to fit its region while maintaining aspect ratio
                resized_image = cv2.resize(image, (new_width, new_height))

                # Check if the image fits in the remaining width
                if current_x + new_width > region_width:
                    # If not enough space stop or resize to fit the remaining space
                    break

                # Place the resized image in the region image
                start_y = (region_height - new_height) // 2  # Center vertically
                region_image[start_y:start_y+new_height, current_x:current_x+new_width] = resized_image

                # Update the starting x position for the next image
                current_x += new_width


            canvas[region[0], region[1]] = region_image

    return canvas
'''