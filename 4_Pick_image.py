import os
import shutil

# 1.读取文件列表，获取对应文件名（输入读取文件路径和保存文件路径）
data_root = '/home/flyingbird/Flyingbird/Test'

train_path = os.path.join(data_root, 'Sets_list/train_set.txt')
val_path = os.path.join(data_root, 'Sets_list/val_set.txt')
test_path = os.path.join(data_root, 'Sets_list/test_set.txt')

image_file = '/home/flyingbird/Flyingbird/Test/images/'
save_path = '/home/flyingbird/Flyingbird/Test/Sets_images/Train_set'
val_file = '/home/flyingbird/Flyingbird/Test/Sets_images/Val_set'
test_file = '/home/flyingbird/Flyingbird/Test/Sets_images/Test_set'

# 1.1得到训练集文件名
with open(train_path, 'r') as f:
    train_images_list = []
    for i in f.readlines():
        train_images_list.append(i.strip().split(' ')[1] + '.jpg')
    train_images_list = train_images_list[1:]

# 1.2 得到验证集文件名
with open(val_path, 'r') as f:
    val_images_list = []
    for i in f.readlines():
        val_images_list.append(i.strip().split(' ')[1] + '.jpg')
    val_images_list = val_images_list[1:]

# 1.3 得到测试集文件名
with open(test_path, 'r') as f:
    test_images_list = []
    for i in f.readlines():
        test_images_list.append(i.strip().split(' ')[1] + '.jpg')
    test_images_list = test_images_list[1:]

print(train_images_list[:5])
print(val_images_list[:5])
print(test_images_list[:5])

# 2.根据文件名复制图像到指定路径

for images_id in train_images_list:
    images_id = os.path.join(image_file, images_id)
    shutil.copy(images_id, save_path)

for images_id in val_images_list:
    images_id = os.path.join(image_file, images_id)
    shutil.copy(images_id, val_file)

for images_id in test_images_list:
    images_id = os.path.join(image_file, images_id)
    shutil.copy(images_id, test_file)

# 3.验证复制后文件个数是否准确
num_train = os.listdir(save_path)
if len(num_train) == 5000:
    print('Results OK')

main_root = '/home/flyingbird/Flyingbird/Test'
image_file = main_root + '/images'
source_path = main_root + '/Sets_list/train_set.txt'

# 建立函数，重复调用
def get_images_name(source_path, save_path):
    """
    input: 原路径列表，保存路径列表（str)
    output: 是否执行成功(yes or no)
    """
    with open(source_path, 'r') as f:
        images_list = []
        for i in f.readlines():
            images_list.append(i.strip().split(' ')[1] + '.jpg')
        images_list = images_list[1:]

    for images_name in images_list:
        images_id = os.path.join(image_file, images_name)
        shutil.copy(images_id, save_path)

    if len(os.listdir(save_path)) == 5000:
        print('Copy Success')
