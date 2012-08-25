import os

class RavlykImage(object):
    def __init__(self, path, poi=None):
        super(RavlykImage, self).__init__()
        self.path = path
        self.filename = os.path.split(path)[1]
        self.poi = poi or []