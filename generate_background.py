#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成4:3竖版背景图
"""

from PIL import Image, ImageDraw
import os

def create_gradient_background(width, height, color1=(135, 206, 235), color2=(70, 130, 180)):
    """创建渐变背景"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def main():
    # 创建data/images目录（如果不存在）
    os.makedirs('data/images', exist_ok=True)
    
    # 设置图片尺寸（4:3竖版）
    width = 900   # 3
    height = 1200  # 4
    
    # 创建渐变背景
    image = create_gradient_background(width, height)
    
    # 保存图片
    output_path = 'data/images/background.jpg'
    image.save(output_path, quality=95)
    print(f'背景图片已保存到：{output_path}')
    print(f'尺寸：{width}x{height} (4:3竖版)')

if __name__ == '__main__':
    main() 