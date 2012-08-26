from PIL import Image
import os

class RavlykImage(object):
    poi = (None, None)

    def __init__(self, path):
        super(RavlykImage, self).__init__()
        self.path = path
        self.filename = os.path.split(path)[1]
        image = Image.open(path)
        self.size = image.size
