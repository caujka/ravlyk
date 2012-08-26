from PIL import Image
from math import trunc
import os
from shutil import copyfile
from image import RavlykImage
from whichtransform import WhichTransform

def transform(src_image, dest_image, dest_dir):
    poi = dest_image.poi + src_image.poi
    if None in poi:
        print "No way"
        return

    t = WhichTransform(src_image.poi, dest_image.poi)
    scale = t.scale()
    angle = t.rotation()

    original = Image.open(dest_image.path)
    orig_x, orig_y = src_image.size
    new_x, new_y = trunc(orig_x * scale), trunc(orig_y * scale)
    transformed = original.resize((new_x, new_y), resample=Image.ANTIALIAS)
    transformed = transformed.rotate(angle, resample=Image.BICUBIC)
    offset_x = (dest_image.poi[0][0] - src_image.poi[0][0])
    offset_y = (dest_image.poi[0][1] - src_image.poi[0][1])

    transformed = transformed.crop((offset_x, offset_y, orig_x + offset_x, orig_y + offset_y))

    transformed.save(os.path.join(dest_dir, dest_image.filename), "JPEG")


def transform_images(images, dest_dir):
    src_image = images[0]
    copyfile(src_image.path, os.path.join(dest_dir, src_image.filename))
    for image in images[1:]:
        transform(src_image, image, dest_dir)


image0 = RavlykImage('images/IMG_5961.JPG')
image1 = RavlykImage('images/IMG_5962.JPG')
image2 = RavlykImage('images/IMG_5963.JPG')
image3 = RavlykImage('images/IMG_5964.JPG')

p1_0 = (305, 318)
p1_1 = (303, 293)
p1_2 = (308, 314)
p1_3 = (328, 312)

p2_0 = (303, 561)
p2_1 = (302, 539)
p2_2 = (305, 564)
p2_3 = (326, 558)

image0.poi = (p1_0, p2_0)
image1.poi = (p1_1, p2_1)
image2.poi = (p1_2, p2_2)
image3.poi = (p1_3, p2_3)
image4.poi = (p1_4, p2_4)

#transform(image1, image2, '/home/ego/Projects/khakaton/ravlyk/transformed/')
transform_images([image0, image1, image2, image3], 'transformed/')