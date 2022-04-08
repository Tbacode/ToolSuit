'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-08-23 16:05:49
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-04-07 23:02:44
 * @FilePath     : \ToolSuit\Color_cv2\img_RGB2location.py
'''


import cv2

import numpy as np

# import time


class RGB2Location(object):
    def set_kernel(self, numb):
        return np.ones((numb, numb), np.uint8)

    def run_main(self, img_path, numb):
        Img = cv2.imread(img_path)  #读入一幅图像

        # kernel_2 = np.ones((1, 1), np.uint8)  #2x2的卷积核

        # kernel_3 = np.ones((3, 3), np.uint8)  #3x3的卷积核

        # kernel_4 = np.ones((4, 4), np.uint8)  #4x4的卷积核
        kernel_2 = self.set_kernel(numb)

        if Img is not None:  #判断图片是否读入

            HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  #把BGR图像转换为HSV格式
        '''

        HSV模型中颜色的参数分别是：色调(H)，饱和度(S)，明度(V)

        下面两个值是要识别的颜色范围

        '''

        Lower = np.array([120, 5, 201])  #要识别颜色的下限

        Upper = np.array([120, 17, 215])  #要识别的颜色的上限

        #mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色

        mask = cv2.inRange(HSV, Lower, Upper)

        #下面四行是用卷积进行滤波

        erosion = cv2.erode(mask, kernel_2, iterations=1)

        erosion = cv2.erode(erosion, kernel_2, iterations=1)

        dilation = cv2.dilate(erosion, kernel_2, iterations=1)

        dilation = cv2.dilate(dilation, kernel_2, iterations=1)

        #target是把原图中的非目标颜色区域去掉剩下的图像

        target = cv2.bitwise_and(Img, Img, mask=dilation)

        #将滤波后的图像变成二值图像放在binary中

        ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)

        #在binary中发现轮廓，轮廓按照面积从小到大排列

        # cv2.imshow("binary", binary)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # print("++++++++contours", contours)
        p = 0
        node_list = []

        for i in contours:  #遍历所有的轮廓

            x, y, w, h = cv2.boundingRect(i)  #将轮廓分解为识别对象的左上角坐标和宽、高

            #在图像上画上矩形(图片、左上角坐标、右下角坐标、颜色、线条宽度)

            cv2.rectangle(Img, (x, y), (x + w, y + h), (
                0,
                255,
            ), 3)

            # 输出图像矩形中间坐标点
            # print("中心坐标：{0},{1}".format(str(x+w/2), str(y+h/2)))
            # print((x + w / 2, y + h / 2))
            node_list.append((x + w / 2, y + h / 2))

            #给识别对象写上标号

            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(Img, str(p), (x - 10, y + 10), font, 1, (0, 0, 255),
                        2)  #加减10是调整字符位置

            p += 1

            # print ('黄色方块的数量是',p,'个')#终端输出目标数量

            # cv2.imshow('target', target)

            # cv2.imshow('Mask', mask)

            # cv2.imshow("prod", dilation)

            # cv2.imshow('Img', Img)

        cv2.imwrite('Img.png', Img)  #将画上矩形的图形保存到当前目录

        return node_list


if __name__ == '__main__':
    rgb = RGB2Location()
    rgb_node = rgb.run_main(
        r"C:\Users\xt875\Documents\airtest\Color_airtest.air\screen2.jpg", 4)
    print(rgb_node)

    # Img = cv2.imread(
    #     r"C:\Users\xt875\Documents\ToolSuit\notebook\screen2.jpg")  #读入一幅图像

    # kernel_2 = np.ones((1, 1), np.uint8)  #2x2的卷积核

    # kernel_3 = np.ones((3, 3), np.uint8)  #3x3的卷积核

    # kernel_4 = np.ones((4, 4), np.uint8)  #4x4的卷积核

    # if Img is not None:  #判断图片是否读入

    #     HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  #把BGR图像转换为HSV格式
    # '''

    # HSV模型中颜色的参数分别是：色调(H)，饱和度(S)，明度(V)

    # 下面两个值是要识别的颜色范围

    # '''

    # Lower = np.array([120, 5, 201])  #要识别颜色的下限

    # Upper = np.array([120, 17, 215])  #要识别的颜色的上限

    # #mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色

    # mask = cv2.inRange(HSV, Lower, Upper)

    # #下面四行是用卷积进行滤波

    # erosion = cv2.erode(mask, kernel_2, iterations=1)

    # erosion = cv2.erode(erosion, kernel_2, iterations=1)

    # dilation = cv2.dilate(erosion, kernel_2, iterations=1)

    # dilation = cv2.dilate(dilation, kernel_2, iterations=1)

    # #target是把原图中的非目标颜色区域去掉剩下的图像

    # target = cv2.bitwise_and(Img, Img, mask=dilation)

    # #将滤波后的图像变成二值图像放在binary中

    # ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)

    # #在binary中发现轮廓，轮廓按照面积从小到大排列

    # # cv2.imshow("binary", binary)

    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL,
    #                                        cv2.CHAIN_APPROX_SIMPLE)

    # print("++++++++contours", contours)
    # p = 0

    # for i in contours:  #遍历所有的轮廓

    #     x, y, w, h = cv2.boundingRect(i)  #将轮廓分解为识别对象的左上角坐标和宽、高

    #     #在图像上画上矩形(图片、左上角坐标、右下角坐标、颜色、线条宽度)

    #     cv2.rectangle(Img, (x, y), (x + w, y + h), (0,255,), 3)

    #     # 输出图像矩形中间坐标点
    #     # print("中心坐标：{0},{1}".format(str(x+w/2), str(y+h/2)))
    #     print((x + w / 2, y + h / 2))

    #     #给识别对象写上标号

    #     font = cv2.FONT_HERSHEY_SIMPLEX

    #     cv2.putText(Img, str(p), (x - 10, y + 10), font, 1, (0, 0, 255),
    #                 2)  #加减10是调整字符位置

    #     p += 1

    #     # print ('黄色方块的数量是',p,'个')#终端输出目标数量

    #     # cv2.imshow('target', target)

    #     # cv2.imshow('Mask', mask)

    #     # cv2.imshow("prod", dilation)

    #     # cv2.imshow('Img', Img)

    # cv2.imwrite('Img.png', Img)  #将画上矩形的图形保存到当前目录
