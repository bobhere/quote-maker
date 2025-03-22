#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成测试用的背景图片
"""

from PIL import Image, ImageDraw
import random
import os

def create_gradient_background(width=1920, height=1080, color1=None, color2=None):
    """创建渐变背景图片"""
    if color1 is None:
        color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if color2 is None:
        color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 确保utils/test_images目录存在
    os.makedirs('utils/test_images', exist_ok=True)
    
    # 保存图片
    output_file = 'utils/test_images/test_background.png'
    image.save(output_file)
    print(f'测试背景图片已生成：{output_file}')
    return output_file

if __name__ == '__main__':
    # 生成柔和的蓝色渐变背景
    create_gradient_background(
        color1=(100, 181, 246),  # 浅蓝色
        color2=(30, 136, 229)    # 深蓝色
    ) 