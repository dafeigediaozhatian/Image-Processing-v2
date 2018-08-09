import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

#% matplotlib inline

# 读取图片和保存图片路径
mask_read_path = 'Mask_RCNN'

PSPNet = 'PSPNet/color'

mask_save_path = 'Image_Fusion'

# 路径文件名遍历，排序
read_list = os.listdir(mask_read_path)
read_list.sort()
PSP_list = os.listdir(PSPNet)
PSP_list.sort()

# print(read_list[:5])
# print(PSP_list[:5])


image_list = PSP_list[:2]
mask_list = read_list[:2]

image, Mask, N = read_image(image_list[0], mask_list[0])

# 读取图片和掩码文件，输出图像、掩码和操作掩码个数
def read_image(image, mask):
    image = os.path.join('PSPNet/color', image)
    # image = os.path.join('Orinigal_image', image)

    mask = os.path.join('Mask_RCNN', mask)

    image = cv2.imread(image, 1)
    Mask = np.load(mask)

    # print(Mask.shape)

    Mask.dtype = 'uint8'
    Mask = Mask + 0

    N = Mask.shape[2]

    return image, Mask, N

# 随机建立颜色元组输出
import colorsys
import random

def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

# 将掩码操作加入image中
def apply_mask(image, mask, color, alpha=0.5):
    """
    Apply the given mask to the image.
    """
    for c in range(3):
        # image[:, :, c] = np.where(mask == 1, image[:, :, c] * (1 - alpha) + alpha * color[c] * 255, image[:, :, c])
        # image[:, :, c] = np.where(mask == 1, 0.5 * 255, image[:, :, c])
        image[:, :, c] = np.where(mask == 1, color[c] * 255, image[:, :, c])

    return image

# 对图像进行多个mask操作
def add_mask(N, Mask, image, colors):
    # colors = random_colors(3)
    for i in range(N):
        color = colors[i]
        mask = Mask[:, :, i]

        image = apply_mask(image, mask, color)

    return image

# 显示图片
def show_image(image):
    # for i in range(N):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
image = PSP_list[:10]
mask = read_list[:10]

image, Mask, N = read_image(image, mask)

#show_image(image)
colors = random_colors(N)
#print(colors)

image = add_mask(N, Mask, image, colors)

show_image(image)
"""

# np.where 使用例子
a = np.array([[0, 1, 2, 5, 3, 1],
              [0, 1, 2, 5, 3, 1]])
b = np.array([[1, 2, 4, 5, 3, 2],
              [1, 2, 4, 5, 3, 2]])
c = np.array([0, 1, 0, 0, 1, 1])

d = np.where(c == 1, a * 0.5 + 0.5 * 20, b)

# 文件夹名列表
image_list = PSP_list
mask_list = read_list

# 读取文件，进行掩码操作处理
for i in range(len(image_list)):
    image, Mask, N = read_image(image_list[i], mask_list[i])

    # show_image(image)
    # 加入掩码图像
    colors = random_colors(N)
    image = add_mask(N, Mask, image, colors)

    # 保存到对应路径
    save_path = os.path.join(mask_save_path, image_list[i])
    cv2.imwrite(save_path, image)
    if i % 100 == 0:
        # print("the %d image named %s has been saved" % (i, image_list[i]))
        print("%d images has been saved" % (i))
    if i == 999:
        print("process over")