
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
from os import listdir
from os.path import isfile, join

from PIL import Image

"""
absPath = os.path.abspath('.')
syspath = os.name

# ::CY::M-08::01
# ~/CY/M-08/01/..
path_arr = ['CY', 'M-08', '01']
appendPath = path_arr[0] + '/' + path_arr[1] + '/' + path_arr[2];
last_path = os.path.join(absPath, appendPath)
final_path = os.path.join(last_path, '01.png')

#f = open(final_path, "wb")
#f.read()
# f.close()

final_dir = '/Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png'
img1 = Image.open(final_dir)
img2 = Image.open('/Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png')
img1.show()
img2.show()


# store the all files to list
# onlyfiles = [f for f in listdir(last_path) if isfile(join(last_path, f))]

# open(onlyfiles[0])

    

print(absPath)
print(syspath)

print(final_path)
"""

def main():
    os.system('open /Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png')
    os.system('open /Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png')

# open -a Preview /Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png /Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png

