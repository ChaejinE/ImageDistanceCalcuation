import cv2
import numpy as np
import os
import yaml

class MatrixCalculator:
    def __init__(self):
        pass
    
    def calculate(self):
        pass
    
class Homography(MatrixCalculator):
    def __init__(self, src_pts=None, dst_pts=None):
        super().__init__()
        if src_pts is None and dst_pts is None:
            self._src = src_pts
            self._dst = dst_pts
        else:
            self._src = np.float32(src_pts).reshape(-1, 1, 2)
            self._dst = np.float32(dst_pts).reshape(-1, 1, 2)
        self.matrix = None
    
    def get_src_pts(self):
        return self._src
    
    def get_dst_pts(self):
        return self._dst
    
    def get_matching_pts(self):
        return list(zip(self._src, self._dst))
    
    def calculate(self):
        try:
            matrix, _ = cv2.findHomography(srcPoints=self._src, dstPoints=self._dst,
                                           method=cv2.RANSAC)
        except Exception as e:
            print(e)
            return None
        return matrix
        
    def __call__(self, src_pts, dst_pts):
        self.__init__(src_pts=src_pts, dst_pts=dst_pts)
        
        os.makedirs("./matrix", exist_ok=True)
        matrix = self.calculate()
        if matrix is not None:
            with open("./matrix/homography.yaml", 'w') as f:
                matrix_yaml = {'homography': matrix.tolist(),
                               'inv_homography':np.linalg.inv(matrix).tolist(),
                               'src': src_pts,
                               'dst': dst_pts}
                yaml.safe_dump(matrix_yaml, f, default_flow_style=False, sort_keys=False)
        
if __name__ == "__main__":
    src_pts = [(1, 2), (3, 4), (4, 5), (5, 6)]
    dst_pts = [(10, 20), (30, 40), (40, 50), (50, 60)]
    matrix = Homography(src_pts, dst_pts)
    # matrix.calculate()
    matrix(src_pts, dst_pts)