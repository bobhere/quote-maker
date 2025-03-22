#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据管理模块：处理标签页之间的数据共享
"""

import logging
import os
import pandas as pd
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage, QPixmap

logger = logging.getLogger(__name__)

class TextItem:
    """文本项类"""
    def __init__(self, text, font_family=None, font_size=None, color=None):
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        
    def __str__(self):
        return self.text

class DataManager(QObject):
    """数据管理类，处理标签页间的数据共享"""
    
    # 定义信号
    image_changed = Signal(str)  # 图片改变信号（传递图片路径）
    texts_changed = Signal(list)  # 文本改变信号
    current_index_changed = Signal(int, int)  # 当前索引改变信号（当前索引，总数）
    
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self._image_path = None
        self._texts = []  # 文本项列表
        self._current_index = -1
        
        # 创建数据目录
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.texts_dir = os.path.join(self.data_dir, 'texts')
        self.images_dir = os.path.join(self.data_dir, 'images')
        self.outputs_dir = os.path.join(self.data_dir, 'outputs')
        
        try:
            for dir_path in [self.texts_dir, self.images_dir, self.outputs_dir]:
                os.makedirs(dir_path, exist_ok=True)
            self.monitor.info_occurred.emit("数据目录初始化完成")
        except Exception as e:
            self.monitor.error_occurred.emit(f"创建数据目录失败: {str(e)}")
        
    def set_image(self, image_path: str):
        """设置当前图片"""
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"找不到图片文件: {image_path}")
            
            # 检查文件类型
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                raise ValueError("不支持的图片格式")
            
            # 如果图片不在images目录中，复制到images目录
            if not image_path.startswith(self.images_dir):
                new_path = os.path.join(self.images_dir, os.path.basename(image_path))
                import shutil
                shutil.copy2(image_path, new_path)
                image_path = new_path
                self.monitor.info_occurred.emit(f"图片已复制到images目录: {os.path.basename(new_path)}")
            
            self._image_path = image_path
            self.image_changed.emit(image_path)
            logger.debug(f"设置新图片：{image_path}")
            
        except Exception as e:
            error_msg = f"设置图片失败：{str(e)}"
            logger.error(error_msg)
            self.monitor.error_occurred.emit(error_msg)
            raise
        
    def get_image(self) -> str:
        """获取当前图片路径"""
        return self._image_path
        
    def set_texts(self, texts: list):
        """设置文本列表"""
        try:
            if not texts:
                self.monitor.warning_occurred.emit("文本列表为空")
                
            # 将普通文本转换为TextItem对象
            text_items = []
            for text in texts:
                if isinstance(text, str):
                    text_items.append(TextItem(text))
                elif isinstance(text, TextItem):
                    text_items.append(text)
                else:
                    raise ValueError(f"不支持的文本类型：{type(text)}")
            
            self._texts = text_items
            self.texts_changed.emit(text_items)
            
            if text_items:
                self.set_current_index(0)  # 设置为第一条
                self.monitor.info_occurred.emit(f"已加载 {len(text_items)} 条文本")
            else:
                self.set_current_index(-1)
                
            logger.debug(f"设置文本列表，共 {len(text_items)} 条")
            
        except Exception as e:
            error_msg = f"设置文本列表失败：{str(e)}"
            logger.error(error_msg)
            self.monitor.error_occurred.emit(error_msg)
            raise
            
    def get_texts(self) -> list:
        """获取文本列表"""
        return self._texts
        
    def get_current_text(self) -> str:
        """获取当前文本"""
        if 0 <= self._current_index < len(self._texts):
            return str(self._texts[self._current_index])
        return None
        
    def set_current_index(self, index: int):
        """设置当前文本索引"""
        if index != self._current_index and -1 <= index < len(self._texts):
            logger.debug(f"切换到第 {index + 1} 条文本")
            self._current_index = index
            self.current_index_changed.emit(index, len(self._texts))
            
    def next_text(self):
        """切换到下一条文本"""
        if self._current_index < len(self._texts) - 1:
            self.set_current_index(self._current_index + 1)
            
    def prev_text(self):
        """切换到上一条文本"""
        if self._current_index > 0:
            self.set_current_index(self._current_index - 1)
            
    def load_excel(self, file_path: str):
        """加载Excel文件"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"找不到Excel文件: {file_path}")
            
            # 检查文件类型
            if not file_path.lower().endswith(('.xlsx', '.xls')):
                raise ValueError("不支持的文件格式，请使用Excel文件(.xlsx或.xls)")
            
            # 如果文件不在texts目录中，复制到texts目录
            if not file_path.startswith(self.texts_dir):
                new_path = os.path.join(self.texts_dir, os.path.basename(file_path))
                import shutil
                shutil.copy2(file_path, new_path)
                file_path = new_path
                self.monitor.info_occurred.emit(f"Excel文件已复制到texts目录: {os.path.basename(new_path)}")
            
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            if df.empty:
                raise ValueError("Excel文件为空")
            
            # 获取第一列作为文本内容，保留换行符
            texts = df.iloc[:, 0].tolist()
            
            # 过滤掉空值和非字符串值，但保留换行符
            texts = [str(text).strip('\t ') for text in texts if pd.notna(text)]  # 只去除首尾的制表符和空格，保留换行符
            
            if not texts:
                raise ValueError("没有找到有效的文本内容")
            
            # 设置文本列表
            self.set_texts(texts)
            
            self.monitor.info_occurred.emit(f"成功加载Excel文件：{os.path.basename(file_path)}")
            logger.info(f"成功加载Excel文件：{file_path}")
            
        except Exception as e:
            error_msg = f"加载Excel文件失败：{str(e)}"
            logger.error(error_msg)
            self.monitor.error_occurred.emit(error_msg)
            raise
            
    def clear(self):
        """清除所有数据"""
        logger.debug("清除所有数据")
        self._image_path = None
        self._texts = []
        self._current_index = -1
        self.image_changed.emit(None)
        self.texts_changed.emit([])
        self.current_index_changed.emit(-1, 0) 