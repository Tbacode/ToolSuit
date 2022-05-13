'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-05 17:04:49
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-05 18:29:53
'''
import cv2
import pyocr
from PIL import Image as PI
import io
import os
from cnocr import CnOcr
import warnings
warnings.filterwarnings("ignore")

# 识别中文或数字
ocr = CnOcr()

# image_src = 'images'
img_list = [r'C:\Users\talefun\Documents\ToolSuit\test\test4\images\xhs.jpg']


# for name in os.walk(image_src):
#     img_list = name[2]
#     print(img_list)

for i in img_list:
    images_url = i
    # img = cv2.imread(images_url)
    with open(images_url, 'rb') as fp:
        a = fp.read()
    new_img = PI.open(io.BytesIO(a))

    left = 800
    right = 150
    top = 3000
    buttom = 100

    img_x = new_img.crop((left, top, left+right, top+buttom))
    img_x.save("img.png")
    img_text = ocr.ocr(r"C:\Users\talefun\Documents\ToolSuit\img.png")
    new_no = ''
    for j in img_text:
        for m in j[0]:
            new_no += m
    print(f'发票号为：{new_no}')
