import yaml
import numpy as np
import cv2
from point import Point
from processor import ImageProcessor
from mouse import PointCallbacks

class_num = 10

def distance_calc(point, point_kind=None):
    with open("./matrix/homography.yaml", 'r') as f:
        infos = yaml.load(f, Loader=yaml.loader.FullLoader)
    
    x, y = point
    point = np.float32(Point(x, y).get_homogeneous())
    homography_mat, inv_homo_mat = np.float32(infos["homography"]), np.float32(infos["inv_homography"])
    result_point = None
    if point_kind=="real":
        result_point = np.matmul(homography_mat, point)
    else:
        print("img2real")
        result_point = np.matmul(inv_homo_mat, point)
    
    x = result_point[0]/result_point[2]
    y = result_point[1]/result_point[2]

    dist = np.linalg.norm(x - y)
    return dist

def distance_calc_using_mouse(specific_cls=None, d_size=(832, 832)):
    import os
    image_dir = os.getcwd() + "/image"
    processor = ImageProcessor(image_dir, "jpg")
    images = processor.get_labeled_images(label_dir="./label", d_size=d_size, specific_cls=specific_cls)
    
    if len(images) < 1:
        assert "You didn't choose picture"
        
    callback_instance = PointCallbacks(images[0])
    img_points = callback_instance.operate()
    if img_points is None:
        assert "You didn't choose points in the picture"
    
    img = callback_instance.get_image()
    for point in img_points:
        x, y = point.get_coord()
        result = distance_calc((x, y))
        cv2.putText(img, f"Distance : {int(result)} m", org=(x, y+30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=0.5, color=(255, 0, 0), thickness=2)
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def distance_calc_using_label(label_dir="./label", specific_cls=None, d_size=(832, 832)):
    global class_num
    
    import os
    image_dir = os.getcwd() + "/image"
    processor = ImageProcessor(image_dir, "jpg")
    images = processor.get_labeled_images(label_dir=label_dir, d_size=d_size, specific_cls=specific_cls)
    
    if len(images) < 1:
        assert "You didn't choose picture"
    
    label_dict = processor.get_picked_label(specific_label=specific_cls)
    labels = []
    if specific_cls is not None:
        labels.append(label_dict[specific_cls])
    else:
        for i in range(class_num):
            labels.append(label_dict[i])
            
    image = processor.get_picked_image()
    
    for id_labels in labels:
        for label in id_labels:
            cx, cy , w, h = label
            cx, w = cx*d_size[0], w*d_size[0]
            cy, h = cy*d_size[1], h*d_size[1]
            point = Point(cx, cy)
            pt1, pt2 = point.get_YOLO2CV(w, h)
            tl, br = tuple(map(int, pt1)), tuple(map(int, pt2))
            pt1, pt2 = point.transform_ground(tl, br)
            cx = pt1[0] + (pt2[0] - pt1[0]) // 2
            print(cx, pt1[1])
            dist = distance_calc((cx, pt1[1]))
            image = cv2.circle(image, (cx, pt1[1]), 3, color=(0, 0, 255), thickness=-1)
            image = cv2.putText(image, org=(cx+10, pt1[1]+10), text=f"X:{cx}", \
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0))
            image = cv2.putText(image, org=(cx+10, pt1[1]+25), text=f"Y:{pt1[1]}", \
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0))
            image = cv2.putText(image, org=(cx+10, pt1[1]+35), text=f"Distance : {int(dist)} m",\
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0))
    cv2.imshow("test", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
            
if __name__ == "__main__":
    distance_calc_using_label(specific_cls=3)
    # img_point = (151, 212)
    # result = distance_calc(img_point)
    # print(result)