"""
# -*- coding: UTF-8 -*-
from PIL import Image


dir1 = '/Users/htwt/Desktop/maxSubseqSum01.png'
dir2 = '/Users/htwt/Desktop/maxSubseqSum02.png'
img1 = Image.open(dir1);
img2 = Image.open(dir2);
img1.show()
img2.show()
"""

import os

apath = os.path.abspath('.')
syspath = os.name

cypath = os.path.join(apath, 'CY')

print(apath)
print(syspath)

print(cypath)
