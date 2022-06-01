import json
import cv2 as cv
import sys
import os

if __name__ == '__main__':
    if(len(sys.argv)!=2):
        print('Usage: crop_img.py [annotation_file]')
        exit()

    filename = sys.argv[1]
    save_dir = os.path.split(filename)[0]

    os.makedirs(f"{save_dir}/crop_img", exist_ok=True)

    with open(filename) as file:
        content = file.read()
        shapes = json.loads(content)

    # print(shapes[0])
    imgname = shapes[0]["image"]
    anns = shapes[0]["annotations"]

    print(imgname, end="... ")
    img = cv.imread(f"{save_dir}/{imgname}")
    for label in anns:
        # print(label["label"], label["coordinates"])
        print(label["label"], end=", ")
        coord = label["coordinates"]
        x, y, w, h = int(coord['x']), int(coord['y']), int(coord["width"]), int(coord["height"])
        crop_temp = img[y-h//2:y+h//2, x-w//2:x+w//2]
        # cv.imshow("crop_temp",crop_temp)
        # cv.waitKey()
        saveimg = os.path.join(save_dir, f"crop_img/{label['label']}_{imgname}")
        cv.imwrite(saveimg, crop_temp)
    print()