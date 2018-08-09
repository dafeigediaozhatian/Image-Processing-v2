import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import math

#% matplotlib inline

'''
# 选择图像
image_file = 'Image_Fusion/2054.png'
image = cv2.imread(image_file, 1)
'''
## 问题：合并颜色少的区域到临近区域，计算区域像素的中点
'''
- 获取图像中所有像素点的颜色三通道值
- 计算颜色出现频次和各颜色坐标中心点
- 当出现次数少于阈值时，将其颜色转化为坐标中心点距离临近的颜色
- 重新计算颜色区域中心点
- 赋予标签并存储：{坐标，label}
'''

# 获取图像中所有像素点的颜色三通道值和索引位置
image_file = 'Image_Fusion/7169.png'
image = cv2.imread(image_file, 1)

# 计算颜色出现频次
def compute_counts(image):
    dict_rgb = {}
    image = list(image)

    for i in image:
        for j in i:
            if tuple(j) not in dict_rgb:
                dict_rgb[tuple(j)] = 1
            else:
                dict_rgb[tuple(j)] += 1
    return dict_rgb

# 计算各颜色坐标中心点
def compute_point(image):
    dict_point = {}
    dict_rgb = compute_counts(image)
    image = list(image)

    for x in range(len(image)):
        for y in range(len(image[0])):
            if tuple(image[x][y]) not in dict_point:
                dict_point[tuple(image[x][y])] = [x + 1, y + 1]
            else:
                dict_point[tuple(image[x][y])][0] += (x + 1)
                dict_point[tuple(image[x][y])][1] += (y + 1)

    for index in dict_point:
        for i in range(len(dict_point[index])):
            dict_point[index][i] = dict_point[index][i] // dict_rgb[index]

    return dict_point

# 计算中心点花费时间
import time

start_time = time.time()
dict_point = compute_point(image)
cost_time = time.time() - start_time
print(cost_time)

# 计算距离
def distance(x, y):
    dist = math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
    return dist

# 计算中心点距离最小颜色
def compute_distance(dict_point):
    # 设置最大距离
    min_distance = math.sqrt(480 ** 2 + 640 ** 2)

    # 循环遍历，计算一个中点和其他各点的距离
    for i in dict_point:
        for j in dict_point:
            if i != j:
                dist = distance(dict_point[i], dict_point[j])
                if dist < min_distance:
                    min_distance = dist
                    min_index = j
                    # print(min_distance)
                    # print(min_index)
        dict_point[i].append(min_index)
    return dict_point

    # 求取每个点和其他点的最小值，将距离最小对应的元组颜色加入字典

# 当出现次数少于阈值时，将其颜色转化为坐标中心点距离临近的颜色
def modify_rgb(image, pix, to_pix):
    for i in image:
        for j in i:
            if j[0] == pix[0] and j[1] == pix[1] and j[2] == pix[2]:
                j[0] = to_pix[0]
                j[1] = to_pix[1]
                j[2] = to_pix[2]

# 根据阈值选择要处理区域
def threshold(image, dict_rgb, threshold_value, dict_point):
    threshold_value = threshold_value
    for i in dict_rgb:
        if dict_rgb[i] < threshold_value:
            modify_rgb(image, i, dict_point[i][2])

import time

start_time = time.time()
# 获取图片颜色出现次数
dict_rgb = compute_counts(image)

# 获取图像区域中心点坐标
dict_point = compute_point(image)

# 计算距离，更新图像区域最近中心点
dict_point = compute_distance(dict_point)

# 根据阈值修改rgb值
threshold(image, dict_rgb, 15000, dict_point)

cost_time = time.time() - start_time
print(cost_time)

compute_counts(image)

cv2.namedWindow('rose', cv2.WINDOW_NORMAL)
cv2.imshow('rose', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 赋予标签并存储：{坐标，label}
compute_point(image)

# 建立PSPnet标签索引列表

'''
# 建立MaskRCNN标签索引列表
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']
'''

