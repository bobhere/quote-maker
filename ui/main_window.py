#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口模块
"""

import logging
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from .content_tab import ContentTab
from .style_tab import StyleTab
from .help_dialog import HelpDialog
from core.data_manager import DataManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, monitor):
        super().__init__()
        # 保存监视器引用
        self.monitor = monitor
        # 创建数据管理器
        self.data_manager = DataManager(self.monitor)
        self.init_ui()
        
        # 连接数据管理器的信号
        self.data_manager.image_changed.connect(self.on_image_changed)
        self.data_manager.texts_changed.connect(self.on_texts_changed)
        self.data_manager.current_index_changed.connect(self.on_current_index_changed)
        
        # 连接监视器信号
        self.monitor.info_occurred.connect(self.show_info)
        self.monitor.warning_occurred.connect(self.show_warning)
        self.monitor.error_occurred.connect(self.show_error)
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
        
        logger.info("主窗口初始化完成")
        
    def init_ui(self):
        """初始化界面"""
        # 设置窗口基本属性
        self.setWindowTitle("Quote Maker")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                background-color: #4a90e2;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5f9e;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QFrame#sidebar {
                background-color: white;
                border-right: 1px solid #e0e0e0;
            }
            QPushButton#nav-button {
                border-radius: 8px;
                padding: 15px;
                text-align: left;
                background-color: transparent;
                color: #666666;
            }
            QPushButton#nav-button:checked {
                background-color: #f0f7ff;
                color: #4a90e2;
            }
            QPushButton#help-button {
                border-radius: 8px;
                padding: 15px;
                text-align: left;
                background-color: transparent;
                color: #666666;
                border-top: 1px solid #e0e0e0;
                margin-top: 10px;
            }
            QPushButton#help-button:hover {
                background-color: #f0f7ff;
                color: #4a90e2;
            }
        """)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建侧边栏
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)
        
        # 添加Logo
        logo_label = QLabel("Quote Maker")
        logo_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4a90e2;
            padding-bottom: 24px;
        """)
        sidebar_layout.addWidget(logo_label)
        
        # 创建导航按钮
        self.content_btn = QPushButton("内容创作")
        self.content_btn.setObjectName("nav-button")
        self.content_btn.setCheckable(True)
        self.content_btn.setChecked(True)
        
        self.style_btn = QPushButton("样式设计")
        self.style_btn.setObjectName("nav-button")
        self.style_btn.setCheckable(True)
        
        sidebar_layout.addWidget(self.content_btn)
        sidebar_layout.addWidget(self.style_btn)
        sidebar_layout.addStretch()
        
        # 添加帮助按钮
        help_btn = QPushButton("使用帮助")
        help_btn.setObjectName("help-button")
        help_btn.clicked.connect(self.show_help)
        sidebar_layout.addWidget(help_btn)
        
        main_layout.addWidget(sidebar)
        
        # 创建内容区域
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(24, 24, 24, 24)
        
        # 使用QStackedWidget
        self.stack_widget = QStackedWidget()
        self.content_tab = ContentTab(self.data_manager)  # 传入数据管理器
        self.style_tab = StyleTab(self.data_manager, self.monitor)     # 传入数据管理器和监视器
        self.stack_widget.addWidget(self.content_tab)
        self.stack_widget.addWidget(self.style_tab)
        content_layout.addWidget(self.stack_widget)
        
        main_layout.addWidget(content_area)
        
        # 连接信号
        self.content_btn.clicked.connect(lambda: self.switch_page(0))
        self.style_btn.clicked.connect(lambda: self.switch_page(1))
        
        # 加载系统字体
        self.style_tab.load_system_fonts()
        
    def switch_page(self, index):
        """切换页面"""
        self.stack_widget.setCurrentIndex(index)
        self.content_btn.setChecked(index == 0)
        self.style_btn.setChecked(index == 1)
        logger.debug(f"切换到页面 {index}")
        
    def show_info(self, message):
        """显示信息"""
        self.statusBar().showMessage(message, 3000)  # 显示3秒
        
    def show_warning(self, message):
        """显示警告"""
        self.statusBar().showMessage(f"警告: {message}", 5000)  # 显示5秒
        
    def show_error(self, message):
        """显示错误"""
        self.statusBar().showMessage(f"错误: {message}", 10000)  # 显示10秒
        
    def on_image_changed(self, image_path):
        """处理图片改变事件"""
        logger.debug(f"图片已更改: {image_path}")
        self.monitor.info_occurred.emit(f"已加载图片: {os.path.basename(image_path)}")
        
    def on_texts_changed(self, texts):
        """处理文本改变事件"""
        logger.debug(f"文本已更改，共 {len(texts)} 条")
        self.monitor.info_occurred.emit(f"已加载 {len(texts)} 条文本")
        
    def on_current_index_changed(self, index, total):
        """处理当前文本索引改变事件"""
        logger.debug(f"当前文本索引: {index + 1}/{total}")
        if index >= 0:
            self.monitor.info_occurred.emit(f"当前文本: {index + 1}/{total}")
        
    def show_help(self):
        """显示帮助对话框"""
        logger.debug("打开帮助对话框")
        help_dialog = HelpDialog(self)
        help_dialog.exec_() 