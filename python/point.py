class Point:
    def __init__(self, x=None, y=None):
        self._x = x
        self._y = y
        
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_coord(self):
        return (self._x, self._y)
    
    def get_homogeneous(self):
        return (self._x, self._y, 1)
    
    def _transform_Yolo2CV(self, w, h):
        tl_x, tl_y = self._x - (w/2.), self._y - (h/2.)
        br_x, br_y = self._x + (w/2.), self._y + (h/2.)
        return (tl_x, tl_y), (br_x, br_y)
    
    def get_YOLO2CV(self, w, h):
        return self._transform_Yolo2CV(w, h)
    
    @staticmethod
    def transform_ground(tl, br):
        from copy import deepcopy
        bl = [0, 0]
        bl[0], bl[1] = deepcopy(tl[0]), deepcopy(br[1])
        return tuple(bl), deepcopy(br)
    
    def trasform_Bbox2ImgCoord():
        pass
    
    def transform_Cam2ImgCoord():
        pass
        
    
    