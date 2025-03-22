#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本处理模块
负责Excel文件的读取和文本内容的处理
"""

import os
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TextContent:
    """文本内容数据类"""
    chinese: str
    english: Optional[str] = None
    
class TextProcessor:
    """文本处理器"""
    
    def __init__(self):
        """初始化文本处理器"""
        self.file_path: str = ""
        self.texts: List[TextContent] = []
        self.has_english: bool = False
        self.total_count: int = 0
        
    def load_excel(self, file_path: str) -> bool:
        """
        加载Excel文件
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            bool: 是否加载成功
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在：{file_path}")
                
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 验证文件格式
            if df.empty:
                raise ValueError("Excel文件为空")
                
            if len(df.columns) == 0:
                raise ValueError("Excel文件格式错误：没有列")
                
            # 获取列名
            columns = df.columns.tolist()
            
            # 检查是否包含英文列
            self.has_english = len(columns) >= 2
            
            # 清空现有数据
            self.texts.clear()
            
            # 处理每一行
            for _, row in df.iterrows():
                chinese_text = str(row[columns[0]]).strip()
                if not chinese_text or pd.isna(chinese_text):
                    continue
                    
                english_text = None
                if self.has_english:
                    english_text = str(row[columns[1]]).strip()
                    if pd.isna(english_text):
                        english_text = None
                        
                self.texts.append(TextContent(
                    chinese=chinese_text,
                    english=english_text
                ))
            
            self.total_count = len(self.texts)
            self.file_path = file_path
            
            return True
            
        except Exception as e:
            raise ValueError(f"处理Excel文件时出错：{str(e)}")
            
    def get_preview(self, count: int = 3) -> List[TextContent]:
        """
        获取预览文本
        
        Args:
            count: 预览条数
            
        Returns:
            List[TextContent]: 预览文本列表
        """
        return self.texts[:count]
        
    def get_file_info(self) -> Dict[str, str]:
        """
        获取文件信息
        
        Returns:
            Dict[str, str]: 文件信息字典
        """
        return {
            'file_name': os.path.basename(self.file_path),
            'text_count': str(self.total_count),
            'has_english': "是" if self.has_english else "否"
        }
        
    def process_text(self, text: str) -> str:
        """
        处理文本
        
        Args:
            text: 原始文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return ""
            
        # 去除首尾空格
        text = text.strip()
        
        # 替换多个空格为单个空格
        text = ' '.join(text.split())
        
        # 处理标点符号
        # TODO: 根据需要添加更多处理规则
        
        return text
        
    def get_text_by_index(self, index: int) -> Optional[TextContent]:
        """
        获取指定索引的文本
        
        Args:
            index: 文本索引
            
        Returns:
            Optional[TextContent]: 文本内容，如果索引无效则返回None
        """
        if 0 <= index < len(self.texts):
            return self.texts[index]
        return None 