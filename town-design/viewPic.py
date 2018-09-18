# 用于浏览结点照片的代码
from PIL import Image


dir1 = '/Users/htwt/Desktop/maxSubseqSum01.png'
dir2 = '/Users/htwt/Desktop/maxSubseqSum02.png'
img1 = Image.open(dir1);
img2 = Image.open(dir2);
img1.show()
img2.show()
