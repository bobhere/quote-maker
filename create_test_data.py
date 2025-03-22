#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成测试数据
"""

import pandas as pd
import os

def create_test_excel():
    """创建测试用的Excel文件"""
    data = {
        '中文': [
            '生活不是等待暴风雨过去，而是学会在雨中翩翩起舞。',
            '把每一个平凡的日子，过成诗一般的生活。',
            '愿你出走半生，归来仍是少年。',
            '不要等待机会，而要创造机会。',
            '心之所向，素履以往。生如逆旅，一苇以航。'
        ],
        '英文': [
            'Life is not about waiting for the storm to pass, but learning to dance in the rain.',
            'Make every ordinary day a poetic life.',
            'May you travel half your life and return still young at heart.',
            "Don't wait for opportunity, create it.",
            'Follow your heart, step forward. Life is a journey, sail with a reed.'
        ]
    }
    
    df = pd.DataFrame(data)
    output_file = 'test.xlsx'
    df.to_excel(output_file, index=False)
    print(f'测试数据已生成：{output_file}')

if __name__ == '__main__':
    create_test_excel() 