from cv2 import polarToCart
from processor import ImageProcessor
from mouse import PointCallbacks
from matrix import Homography
from point import Point
import os

class HomographyCalculator:
    def __init__(self, image_ext):
        self.image_dir = os.getcwd()
        self.image_ext = image_ext
        self.processor = ImageProcessor(f"{self.image_dir}/image", self.image_ext)
        self.homography_matrix = None

    def calc_maually(self, real_points, labeld_image=True, specific_cls=None):
        images = None
        if labeld_image:
            images = self.processor.get_labeled_images(is_show=True, d_size=(832, 832), specific_cls=specific_cls)
        else:
            images = self.processor.get_images(is_show=True, d_size=(832, 832))
        
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
        result = homography(real_points, img_points)
        
        return result
    
    def calc_auto(self, real_points):
        images = self.processor.get_images(is_show=True, d_size=(832, 832))
        
        real_points = tuple(map(lambda x: Point(x[0], x[1]).get_coord(), real_points))
        result = None
        for image in images:
            corners = self.processor.get_corners(image, matrix_size=(19, 19), is_show=True)
            if corners is not None:
                img_points = tuple(map(lambda x: x.get_coord(), corners))
                homography = Homography()
                result = homography(real_points, img_points)
            else:
                print("Prgram didn't get corners")
                continue
            
        return result
        
        
        
    
if __name__ == "__main__":
    real = [(-2, 1), (-1, 1), (1, 2), (2, 2)]
    calculator = HomographyCalculator(image_ext="jpg")
    # calculator.calc_maually(real, labeld_image=True, specific_cls=3)
    
    import random
    x = [random.randrange(0, 500, 2) for p in range(361)]
    y = [random.randrange(0, 500, 2) for p in range(361)]
    real = list(zip(x, y))
    result = calculator.calc_auto(real)
