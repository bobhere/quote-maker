#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
帮助对话框模块
"""

import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
import markdown

class HelpDialog(QDialog):
    """帮助对话框类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("使用帮助")
        self.setMinimumSize(800, 600)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QTextBrowser {
                border: none;
                font-size: 14px;
                line-height: 1.6;
            }
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
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 创建文本浏览器
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        layout.addWidget(self.text_browser)
        
        # 创建关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        close_button.setFixedWidth(100)
        
        # 添加按钮布局
        button_layout = QVBoxLayout()
        button_layout.addWidget(close_button)
        button_layout.setAlignment(close_button, Qt.AlignCenter)
        layout.addLayout(button_layout)
        
        # 加载帮助文档
        self.load_help_content()
        
    def load_help_content(self):
        """加载帮助文档内容"""
        try:
            # 读取Markdown文件
            docs_path = os.path.join(os.getcwd(), "docs", "使用说明.md")
            with open(docs_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 转换Markdown为HTML
            html_content = markdown.markdown(
                md_content,
                extensions=['tables', 'fenced_code']
            )
            
            # 添加CSS样式
            styled_html = f"""
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    padding: 0 10px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 25px;
                }}
                ul, ol {{
                    padding-left: 25px;
                }}
                li {{
                    margin: 5px 0;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: Consolas, Monaco, monospace;
                }}
            </style>
            {html_content}
            """
            
            # 设置HTML内容
            self.text_browser.setHtml(styled_html)
            
        except Exception as e:
            self.text_browser.setPlainText(f"加载帮助文档失败：{str(e)}") 