import math

""" In all functions point is a tuple (x,y)
"""

def _distance(p1, p2):
    "distance between point1 and point2"
    dx=p2[0] - p1[0]
    dy=p2[1] - p1[1]
    return _length(dx, dy)

def _length(x,y):
    return math.sqrt(x*x+y*y)    

class WhichTransform:
    """ Gets source two pairs of points: where they are
    and where they should be, and calculates a transformation.
    """

    def __init__(self, p1_source, p2_source, p1_dest, p2_dest):
        self.x1_src = p1_source[0]
        self.y1_src = p1_source[1]
        self.x2_src = p2_source[0]
        self.y2_src = p2_source[1]
        self.x1_dst = p1_dest[0]
        self.y1_dst = p1_dest[1]
        self.x2_dst = p2_dest[0]
        self.y2_dst = p2_dest[1]

    def scale(self):
        l_src = _distance((self.x1_src, self.y1_src),
                          (self.x2_src, self.y2_src))
        l_dst = _distance((self.x1_dst, self.y1_dst),
                          (self.x2_dst, self.y2_dst))

        return l_dst/l_src

    def rotation(self):
        dx_src = self.x2_src - self.x1_src
        dy_src = self.y2_src - self.y1_src
        dx_dst = self.x2_dst - self.x1_dst
        dy_dst = self.y2_dst - self.y1_dst

        l_src = _length(dx_src, dy_src)
        l_dst = _length(dx_dst, dy_dst)

        if l_dst == l_src:
            return 0

        return math.degrees(math.acos(
            (dx_src*dx_dst + dy_src*dy_dst) / l_dst / l_src
            ))


    def translation(self):
        dx = self.x1_dst - self.x1_src
        dy = self.y1_dst - self.y1_src
        return (dx, dy)