import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#% matplotlib inline

# 文件路径
ava_file = 'AVA.txt'
segs_file = 'tags.txt'

# 读取Pandas－DataFrame数据
df_ava = pd.read_csv(ava_file, header=None, sep=' ')
df_segs = pd.read_csv(segs_file, header=None, sep=' ')

# 将数据的对应列累加，计算平均得分
df_ava['total_scores'] = df_ava[2] * 1 + df_ava[3] * 2 + df_ava[4] * 3 + \
                         df_ava[5] * 4 + df_ava[6] * 5 + df_ava[7] * 6 + \
                         df_ava[8] * 7 + df_ava[9] * 8 + df_ava[10] * 9 + \
                         df_ava[11] * 10

df_ava['vote_nums'] = df_ava[2] + df_ava[3] + df_ava[4] + \
                      df_ava[5] + df_ava[6] + df_ava[7] + \
                      df_ava[8] + df_ava[9] + df_ava[10] + \
                      df_ava[11]

df_ava['ave_scores'] = df_ava['total_scores'] / df_ava['vote_nums']

# 删除计算列，添加分数列并重命名
df = df_ava.drop(labels=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 'total_scores', 'vote_nums'], axis=1)

df.rename(columns={0: 'index', 1: 'image_id', 12: 'seg_1', 13: 'seg_2'}, inplace=True)
#print(df.rename(columns={0: 'index', 1: 'image_id', 12: 'seg_1', 13: 'seg_2'}, inplace=True))
print(df.head())

# 保存文件
df.to_csv('ava_segs_scores.txt', sep=' ', index=False)

#df.sort_values(by='ave_scores')