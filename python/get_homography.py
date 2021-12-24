from cv2 import polarToCart
from processor import ImageProcessor
from mouse import PointCallbacks
from matrix import Homography
from point import Point
import os

def main(real_points, image_ext):
    image_dir = os.getcwd()
    processor = ImageProcessor(f"{image_dir}/image", image_ext)
    # images = processor.get_images(is_show=True, d_size=(832, 832))
    images = processor.get_labeled_images(is_show=True, d_size=(832, 832))
    
    if len(images) < 1:
        print("You didn't choose picture")
        return
    
    callback_instance = PointCallbacks(images[0])
    img_points = callback_instance.operate()
    if img_points is None:
        print("You didn't choose points in the picture")
        return
    
    img_points = tuple(map(lambda x: x.get_coord(), img_points))
    real_points = tuple(map(lambda x: Point(x[0], x[1]).get_coord(), real_points))

    homography = Homography()
    homography(real_points, img_points)
    
if __name__ == "__main__":
    real = [(-2, 1), (-1, 1), (1, 2), (2, 2)]
    main(real_points=real, image_ext="jpg")