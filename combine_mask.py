import json
import cv2 as cv
import sys
import os
import numpy as np

with open("teeth_rgb.json") as cf:
    content = cf.read()
    color_dict = json.loads(content)[0]

if __name__ == '__main__':
    if(len(sys.argv)!=3):
        print('Usage: combine_mask.py [mask_dir] [ann_file]')
        exit()
    mask_dir = sys.argv[1]
    ann_file = sys.argv[2]

    # mask_dir = "0/crop_mask"
    # ann_file = "0/IMG_7627.xml.json"
    
    save_dir = os.path.split(ann_file)[0]
    
    masklist = sorted([x for x in os.listdir(mask_dir) if ".JPG" in x or ".jpg" or ".png" in x])

    with open(ann_file) as file:
        content = file.read()
        shapes = json.loads(content)

    # print(shapes[0])
    imgname = shapes[0]["image"]
    anns = shapes[0]["annotations"]

    print(imgname, " mask combination...")

    img = cv.imread(f"{save_dir}/{imgname}")
    mask_final = np.zeros(img.shape, np.uint8)

    for label in anns:
        # 11_IMG_7627.JPG
        # print(label["label"], label["coordinates"])
        print(label["label"], end=", ")
        tag = label["label"]
        coord = label["coordinates"]
        x, y, w, h = int(coord['x']), int(coord['y']), int(coord["width"]), int(coord["height"])
        try: 
            mask = cv.imread(f"{mask_dir}/{tag}_{imgname}")
            mask = cv.resize(mask, (mask.shape[1]*2, mask.shape[0]*2), interpolation=cv.INTER_NEAREST)

            # print(mask.shape[:2], h, w)

            mask_b = mask[:,:,0].copy()
            mask_g = mask[:,:,1].copy()

            # print(color_dict[tag])
            mask_final[np.where(mask_b>100)[0]+y-h//2, np.where(mask_b>100)[1]+x-w//2] = color_dict[tag]

        except Exception as e:
            print(e)
    
    cv.imwrite(f"{save_dir}/{imgname[:imgname.find('.')]}.png", mask_final)
