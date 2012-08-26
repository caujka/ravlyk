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

def _cosa(x1, y1, x2, y2):
    l1 = _length(x1, y1)
    l2 = _length(x2, y2)
    if l1==0 or l2==0:
        return 1
    return (x1*x2 + y1*y2) / l1 / l2


class WhichTransform:
    """ Gets source two pairs of points: where they are
    and where they should be, and calculates a transformation.
    """

    def __init__(self, poi_source, poi_dest):
        (p1_source, p2_source) = poi_source
        (p1_dest, p2_dest) = poi_dest
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
        return math.degrees(math.acos(_cosa(dx_src, dy_src, dx_dst, dy_dst)))

    def translation(self):
        dx = self.x1_dst - self.x1_src
        dy = self.y1_dst - self.y1_src
        return (dx, dy)

    def matrix(self):
        dx_src = self.x2_src - self.x1_src
        dy_src = self.y2_src - self.y1_src
        dx_dst = self.x2_dst - self.x1_dst
        dy_dst = self.y2_dst - self.y1_dst
        cosa = _cosa(dx_src, dy_src, dx_dst, dy_dst)
        sina = math.sqrt(1-cosa*cosa)
        (dxx, dyy) = self.translation()
        s = self.scale()

        return (s*cosa, sina, dxx, -sina, s*cosa, dyy)