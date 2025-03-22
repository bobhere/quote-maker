#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
内容创作页面模块
"""

import logging
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QDragLeaveEvent
from PySide6.QtGui import QIcon

logger = logging.getLogger(__name__)

class ContentCard(QFrame):
    """内容卡片组件"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("content-card")
        self.setStyleSheet("""
            QFrame#content-card {
                background-color: white;
                border-radius: 12px;
                padding: 16px;
            }
            QLabel#card-title {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        title_label = QLabel(title)
        title_label.setObjectName("card-title")
        layout.addWidget(title_label)

class ContentTab(QWidget):
    """内容创作页面类"""
    
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # 文本内容区域
        text_card = ContentCard("文本内容")
        text_layout = text_card.layout()
        
        # 文件拖放区域
        self.drop_area = QFrame()
        self.drop_area.setObjectName("drop-area")
        self.drop_area.setStyleSheet("""
            QFrame#drop-area {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                padding: 32px;
                background-color: #fafafa;
            }
            QFrame#drop-area:hover {
                border-color: #4a90e2;
                background-color: #f0f7ff;
            }
        """)
        self.drop_area.setAcceptDrops(True)
        
        drop_layout = QVBoxLayout(self.drop_area)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        # 添加图标
        icon_label = QLabel()
        icon_label.setPixmap(QIcon.fromTheme("document-open").pixmap(48, 48))
        drop_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        # 添加提示文本
        drop_label = QLabel("拖放Excel文件到这里\n或点击选择文件")
        drop_label.setAlignment(Qt.AlignCenter)
        drop_label.setStyleSheet("""
            color: #666666;
            font-size: 14px;
        """)
        drop_layout.addWidget(drop_label)
        
        # 添加选择按钮
        select_file_btn = QPushButton("选择Excel文件")
        select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5f9e;
            }
        """)
        select_file_btn.clicked.connect(self.select_excel)
        drop_layout.addWidget(select_file_btn, alignment=Qt.AlignCenter)
        
        text_layout.addWidget(self.drop_area)
        
        # 文件信息显示
        self.file_info = QLabel()
        self.file_info.setWordWrap(True)
        self.file_info.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            margin-top: 16px;
        """)
        text_layout.addWidget(self.file_info)
        
        # 文本预览区域
        preview_scroll = QScrollArea()
        preview_scroll.setWidgetResizable(True)
        preview_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 16, 0, 0)
        
        preview_label = QLabel("文本预览")
        preview_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 8px;
        """)
        preview_layout.addWidget(preview_label)
        
        self.text_preview = QLabel("暂无文本内容")
        self.text_preview.setWordWrap(True)
        self.text_preview.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            line-height: 1.6;
        """)
        preview_layout.addWidget(self.text_preview)
        preview_layout.addStretch()
        
        preview_scroll.setWidget(preview_widget)
        text_layout.addWidget(preview_scroll)
        
        layout.addWidget(text_card, stretch=1)
        
        # 图片内容区域
        image_card = ContentCard("背景图片")
        image_layout = image_card.layout()
        
        # 图片选择按钮
        select_image_btn = QPushButton("选择图片")
        select_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5f9e;
            }
        """)
        select_image_btn.clicked.connect(self.select_image)
        image_layout.addWidget(select_image_btn)
        
        # 图片预览区域
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setMinimumSize(300, 200)
        self.image_preview.setStyleSheet("""
            QLabel {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        image_layout.addWidget(self.image_preview)
        
        # 图片信息显示
        self.image_info = QLabel()
        self.image_info.setWordWrap(True)
        self.image_info.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            margin-top: 16px;
        """)
        image_layout.addWidget(self.image_info)
        
        layout.addWidget(image_card, stretch=1)
        
        logger.info("内容创作页面初始化完成")
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """处理拖入事件"""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.xlsx', '.xls')):
                event.acceptProposedAction()
                self.drop_area.setStyleSheet("""
                    QFrame#drop-area {
                        border: 2px dashed #4a90e2;
                        border-radius: 8px;
                        padding: 32px;
                        background-color: #f0f7ff;
                    }
                """)
    
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        """处理拖离事件"""
        self.drop_area.setStyleSheet("""
            QFrame#drop-area {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                padding: 32px;
                background-color: #fafafa;
            }
            QFrame#drop-area:hover {
                border-color: #4a90e2;
                background-color: #f0f7ff;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """处理放下事件"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.xlsx', '.xls')):
                self.load_excel_file(file_path)
        self.drop_area.setStyleSheet("""
            QFrame#drop-area {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                padding: 32px;
                background-color: #fafafa;
            }
            QFrame#drop-area:hover {
                border-color: #4a90e2;
                background-color: #f0f7ff;
            }
        """)
    
    def select_excel(self):
        """选择Excel文件"""
        logger.info("打开Excel文件选择对话框")
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel files (*.xlsx *.xls)")
        file_dialog.setDirectory("data/texts")  # 设置默认目录
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            logger.info(f"选择了Excel文件: {file_path}")
            self.load_excel_file(file_path)
    
    def load_excel_file(self, file_path):
        """加载Excel文件"""
        try:
            logger.info(f"开始加载Excel文件: {file_path}")
            # 使用数据管理器加载Excel文件
            self.data_manager.load_excel(file_path)
            
            # 更新文件信息
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            self.file_info.setText(
                f"文件名：{file_name}\n"
                f"大小：{file_size / 1024:.1f} KB"
            )
            
            # 更新文本预览
            self.update_text_preview()
            
            logger.info(f"Excel文件加载成功")
            
        except Exception as e:
            logger.error(f"加载Excel文件失败：{str(e)}")
            self.file_info.setText("文件加载失败")
            
    def update_text_preview(self):
        """更新文本预览"""
        try:
            texts = self.data_manager.get_texts()
            if texts:
                preview_text = "\n\n".join(
                    f"{i+1}. {text}" for i, text in enumerate(texts)
                )
                self.text_preview.setText(preview_text)
                logger.info(f"更新文本预览，共 {len(texts)} 条")
            else:
                self.text_preview.setText("无文本内容")
                logger.info("文本预览为空")
                
        except Exception as e:
            logger.error(f"更新文本预览失败：{str(e)}")
            self.text_preview.setText("预览失败")
    
    def select_image(self):
        """选择图片"""
        logger.info("打开图片选择对话框")
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setDirectory("data/images")  # 设置默认目录
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            logger.info(f"选择了图片: {file_path}")
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """加载图片"""
        try:
            logger.info(f"开始加载图片: {file_path}")
            # 保存图片路径到数据管理器
            self.data_manager.set_image(file_path)
            
            # 更新预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_preview.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                logger.info("图片加载成功")
            else:
                logger.error("无法加载图片")
                
        except Exception as e:
            logger.error(f"加载图片失败：{str(e)}")
            
    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)
        # 如果有图片，重新调整大小
        if self.image_preview.pixmap():
            pixmap = self.image_preview.pixmap()
            scaled_pixmap = pixmap.scaled(
                self.image_preview.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap) 