import cv2
from processor import ImageProcessor
from collections import deque
from copy import deepcopy
from point import Point
from typing import Tuple

class MouseCallbacks:
    def __init__(self, image):
        self.image = image
    
    def eventCallback(self, event, x, y, flags, param):
        pass
    
    def operate(self):
        pass

class PointCallbacks(MouseCallbacks):
    def __init__(self, image) -> None:
        super().__init__(image)
        self.q = deque()
        self.q_coord = deque()
        self.first = True
        cv2.imshow("draw", self.image)
        
    def get_image(self):
        return self.image

    def eventCallback(self, event, x, y, flags, param):
        if self.first:
            self.image = param
            self.first = False
            
        else:
            if event == cv2.EVENT_FLAG_LBUTTON:
                self.q.append(deepcopy(self.image))
                self.image = deepcopy(cv2.circle(self.image, (x, y), 3, color=(0, 0, 255), thickness=-1))
                self.image = deepcopy(cv2.putText(self.image, org=(x+10, y), text=f"X:{x}, Y:{y}",
                                                  fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0)))
                self.q_coord.append(Point(x, y))
                
            elif event == cv2.EVENT_MBUTTONDOWN:
                self.image = self.q.pop()
                self.q_coord.pop()
            
        cv2.imshow("draw", self.image)
        
    def operate(self) -> Tuple[Point]:
        import os
        cv2.setMouseCallback("draw", self.eventCallback, self.image)
        cv2.waitKey()
        os.makedirs("./point", exist_ok=True)
        save_file_name = "test"
        count = 0
        for file in os.listdir("./point"):
            if file.startswith(save_file_name):
                count += 1
        
        cv2.imwrite(f"./point/test{count}.jpg", self.image) if count != 0 else cv2.imwrite(f"./point/test.jpg", self.image)
        cv2.destroyAllWindows()
        
        if len(self.q_coord) == 0:
            return None
        else:
            return tuple(self.q_coord)
            
if __name__ == "__main__":
    import os
    
    image_dir = os.getcwd()
    processor = ImageProcessor(image_dir, "jpeg")
    images = processor.get_images()

    callback_instance = PointCallbacks(images[0])
    points = callback_instance.operate()
    [print(point.get_coord()) for point in points]