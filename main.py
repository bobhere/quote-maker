#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quote Maker - 图文生成器
主程序入口
"""

import sys
import logging
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot
from ui.main_window import MainWindow

class ApplicationMonitor(QObject):
    """应用程序监视器"""
    error_occurred = Signal(str)  # 错误信号
    warning_occurred = Signal(str)  # 警告信号
    info_occurred = Signal(str)  # 信息信号
    
    def __init__(self):
        super().__init__()
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        # 创建logs目录
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # 设置日志文件名（包含时间戳）
        log_file = os.path.join(log_dir, f'quote_maker_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        # 配置日志处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 配置根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # 记录启动信息
        logging.info("日志系统初始化完成")
        
    @Slot(str)
    def on_error(self, message):
        """处理错误"""
        logging.error(message)
        self.error_occurred.emit(message)
        
    @Slot(str)
    def on_warning(self, message):
        """处理警告"""
        logging.warning(message)
        self.warning_occurred.emit(message)
        
    @Slot(str)
    def on_info(self, message):
        """处理信息"""
        logging.info(message)
        self.info_occurred.emit(message)

def main():
    """主程序入口"""
    try:
        logging.info("程序启动...")
        app = QApplication(sys.argv)
        
        # 创建应用监视器
        monitor = ApplicationMonitor()
        
        logging.info("创建应用程序实例...")
        # 设置应用信息
        app.setApplicationName("Quote Maker")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("QuoteMaker")
        app.setOrganizationDomain("quotemaker.com")
        
        logging.info("创建主窗口...")
        # 创建并显示主窗口
        window = MainWindow(monitor)
        logging.info("显示主窗口...")
        window.show()
        
        logging.info("进入事件循环...")
        # 运行应用程序
        return app.exec()
        
    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    logging.info("开始执行main()...")
    sys.exit(main()) 