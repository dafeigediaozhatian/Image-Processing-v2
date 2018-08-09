import os
import cv2
import random
import shutil
import pandas as pd

# 读取完整数据集，转化为df格式
ava_path = "/home/flyingbird/Flyingbird/AVA/AVA_dataset/AVA_with_segs_scores_aesthetic.txt"
df = pd.read_csv(ava_path, sep=' ')

# 随机抽取5000张图像
total_set = df.sample(n=5000, random_state=66)
total_set.info()

# 其中60%图像作为训练集，保存为train_set.txt文件
train_set = total_set.sample(frac=0.6, random_state=66)
train_set.to_csv('train_set.txt', sep=' ', index=None)

# 去掉5000张图中训练集部分
total_set.drop(train_set.index, axis=0, inplace=True)
total_set.info()

# 抽取其中1000张图作为验证集
val_set = total_set.sample(frac=0.5, random_state=66)
val_set.to_csv('val_set.txt', sep=' ', index=None)
val_set.info()

# 去掉验证集，剩余1000张作为测试集合
total_set.drop(val_set.index, axis=0, inplace=True)
test_set = total_set
test_set.to_csv('test_set.txt', sep=' ', index=None)

print(val_set.head())

print(test_set.head())