import os
import time
import pandas as pd

# 读取计算分值后的dataframe文件
ava_path = "/home/flyingbird/Flyingbird/AVA/AVA_dataset/ava_segs_scores.txt"
seg_path = "/home/flyingbird/Flyingbird/AVA/AVA_dataset/tags.txt"

# 读取对应文件并放入列表中
with open(ava_path, 'r') as f1:
    ava = []
    ava_list = f1.readlines()
    for i in ava_list:
        ava.append(i.strip().split(' '))

with open(seg_path, 'r') as f2:
    seg = []
    seg_list = f2.readlines()
    for i in seg_list:
        seg.append(i.strip().split(' '))

# 建立标签的查询字典
seg_dict = {}
for i in seg:
    for j in range(2):
        seg_dict[i[0]] = i[1]


ava = ava[1:]
print(ava[:10])

print(seg[:10])

# 在ＡＶＡ中根据查询字典将数字转换为标签
start_time = time.time()
for i in ava:
    for j in range(2):
        for m in seg:
            if i[j + 2] == m[0]:
                i[j + 2] = m[1]

cost_time = time.time() - start_time
print(cost_time)
# print(ava[:100])
print(ava[:10])

#　将转换标签后的数据写入ｐａｎｄａｓ中，并保存
df_ava = pd.DataFrame(data=ava, columns=['index', 'image_id', 'seg_1', 'seg_2', 'ave_scores'])
print(df_ava.head())
df_ava.to_csv('AVA_with_segs_and_scores.txt', sep=' ', index=False)


# 将scores中大于５和小于５的图分为１和０，保存文本
filename = 'AVA_with_segs_and_scores.txt'
df = pd.read_csv(filename, sep=' ')

df['aesthetic_image'] = 0

df.loc[df.ave_scores > 5, 'aesthetic_image'] = 1

df.to_csv('AVA_with_segs_scores_aesthetic.txt', sep=' ', index=False)