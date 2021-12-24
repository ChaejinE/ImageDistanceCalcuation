import cv2
import os
from point import Point

class Processor:
    def __init__(self, dir) -> None:
        self.dir = dir
        
    def operate(self):
        pass

class ImageProcessor(Processor):
    def __init__(self, dir, file_ext="jpg") -> None:
        super().__init__(dir)
        self._image_dir = self.dir
        self._image_files = [ file for file in os.listdir(self._image_dir) if file.endswith(file_ext)]
        print(f"Got Image files : {self._image_files}")
        print(f"Got Image num : {len(self._image_files)}")
        self._picked_img_file = {}
        
    def get_images(self, mode=cv2.IMREAD_COLOR, d_size=None, is_show=False):
        if mode == "gray":
            mode = cv2.IMREAD_GRAYSCALE
        elif mode == "unchanged":
            mode = cv2.IMREAD_UNCHANGED
            
        images = [ cv2.imread(os.path.join(self._image_dir, name), mode) for name in self._image_files ]
        images = list(map(lambda src: cv2.resize(src, dsize=d_size), images)) if d_size is not None else images
        if is_show:
            for idx, (image, name) in enumerate(zip(images, self._image_files)):
                cv2.imshow(f"({idx}) {name}", image)
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                if key == 32:
                    self._picked_img_file[name] = image
                    return [image]
                
        return images
    
    def get_picked_image(self):
        name = list(self._picked_img_file.keys())[0]
        return self._picked_img_file[name]
    
    def get_picked_label(self, specific_label=None, label_dir="./label"):
        name = list(self._picked_img_file.keys())[0]
        label_name = name[:-4] + ".txt"
        from collections import defaultdict
        label = defaultdict(list)
        with open(os.path.join(label_dir, label_name), 'r') as f:
            for line in f.readlines():
                line = line.strip()
                infos = line.split()
                id, bbox = int(infos[0]), list(map(float, infos[1:]))
                if specific_label is not None and specific_label != id:
                    continue
                label[id].append(bbox)

        return label
    
    def get_labeled_images(self, label_dir="./label", mode=cv2.IMREAD_COLOR, d_size=None, is_show=True, class_num=10, specific_cls=None):
        label_files = os.listdir(label_dir)
        _ = self.get_images(mode=mode, d_size=d_size, is_show=True)
        
        name = list(self._picked_img_file.keys())[0]
        label_name = name[:-4] + ".txt"
        if label_name not in label_files:
            print("Not Exist Label")
            return
        
        from collections import defaultdict
        label = defaultdict(list)
        with open(os.path.join(label_dir, label_name), 'r') as f:
            for line in f.readlines():
                line = line.strip()
                infos = line.split()
                id, bbox = int(infos[0]), list(map(float, infos[1:]))
                label[id].append(bbox)
        
        image = self._picked_img_file[name]
        for id in range(class_num):
            if specific_cls is not None and specific_cls != id:
                continue 
            
            for bbox in label[id]:
                cx, cy , w, h = bbox
                cx, w = cx*d_size[0], w*d_size[0]
                cy, h = cy*d_size[1], h*d_size[1]
                point = Point(cx, cy)
                pt1, pt2 = point.get_YOLO2CV(w, h)
                pt1, pt2 = tuple(map(int, pt1)), tuple(map(int, pt2))
                image = cv2.rectangle(img=image,pt1=pt1, pt2=pt2, color=(20*id, 40*id, 60*id), thickness=2)
            
            if specific_cls == id:
                break
            
        if is_show:
            print(image.shape)
            cv2.imshow("test", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return [image]
                    
    def operate(self):
        pass
    
class VideoProcessor(Processor):
    def __init__(self, dir):
        super().__init__(dir)
        self._video_dir = self.dir
    
    def operate(self):
        pass
    
if __name__ == "__main__":
    image_dir = os.getcwd() + "/image"
    processor = ImageProcessor(image_dir, "jpg")
    # images = processor.get_images(is_show=True)
    processor.get_labeled_images(label_dir="./label", d_size=(832, 832))