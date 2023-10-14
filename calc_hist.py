# -*- coding:utf-8 -*-
"""
Title:使用字典对任意一张二维灰度图像进行直方图统计
Author:He Hulingxiao
Date:2022.10.05
"""
import cv2

def interval_statistics(data, intervals: dict):
    '''
    对数据进行区间统计
    '''
    if len(data) == 0:
        return
    for num in data:
        for interval in intervals.keys():
            lr = tuple(interval.split('~'))
            left, right = int(lr[0]), int(lr[1])
            if left <= num <= right:
                intervals[interval] += 1
    print("直方图统计结果如下：")
    for key, value in intervals.items():
        print("%10s" % key, end='')  # 借助 end=''可以不换行
        print("%10s" % value, end='')  # "%10s" 右对齐
        print('%16s' % '{:.3%}'.format(value * 1.0 / len(data)))

def calHist(X, BINS: int):
    '''
    对灰度图进行直方图统计
    '''
    #构建由不同区间构成的字典
    intervals = {}
    if 0 < BINS <= 256:
        stride = 255 // BINS
        start = 0
        while (start + stride < 256):
            interval = {str(start)+'~'+str(start+stride):0}
            intervals.update(interval)
            start += (stride + 1)
        if start != 256:
            last_interval = {str(start)+'~'+str(255):0}
            intervals.update(last_interval)
    else:
        raise ValueError('划分区间数应是[1,256]的整数')
    #将灰度图像像素映射到字典区间
    interval_statistics(X, intervals)


if __name__ == '__main__':
    img = cv2.imread(r'./img.jpg')
    cv2.imshow('img', img)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('imgGray', imgGray)
    #对于通常的二维图像来说，需要使用ravel()函数将图像处理为一维数据源
    calHist(img.ravel(), 10)
    cv2.waitKey(0)
    cv2.destroyAllWindows()