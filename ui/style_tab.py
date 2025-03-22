#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
样式设计页面模块
"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSpinBox, QComboBox, QColorDialog,
    QFrame, QGraphicsView, QGraphicsScene, QProgressBar,
    QProgressDialog, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontDatabase, QPixmap, QPainter, QImage, QTextBlockFormat, QTextCursor, QTextDocument, QTextCharFormat
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class PreviewCard(QFrame):
    """预览卡片组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("preview-card")
        self.setStyleSheet("""
            QFrame#preview-card {
                background-color: white;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # 预览标题
        title = QLabel("实时预览")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 12px;
        """)
        layout.addWidget(title)
        
        # 预览视图
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("""
            QGraphicsView {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
            }
        """)
        layout.addWidget(self.view)
        
        # 导航按钮
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("上一个")
        self.next_btn = QPushButton("下一个")
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)

class StyleTab(QWidget):
    """样式设计页面类"""
    
    style_changed = Signal()  # 样式改变信号
    
    def __init__(self, data_manager, monitor):
        super().__init__()
        self.data_manager = data_manager
        self.monitor = monitor
        self.style_config = {
            'font_family': 'Arial',
            'font_size': 24,
            'text_color': QColor('#000000'),
            'line_spacing': 1.5,
            'margin_top': 50,
            'margin_bottom': 50,
            'margin_left': 50,
            'margin_right': 50,
            'center_horizontally': True,
            'center_vertically': True
        }
        
        # 添加字体文件夹路径
        self.fonts_dir = os.path.join(os.getcwd(), "fonts")
        os.makedirs(self.fonts_dir, exist_ok=True)
        
        # 存储已加载的自定义字体ID
        self.custom_font_ids = set()
        
        self.init_ui()
        
        # 连接数据管理器信号
        self.data_manager.image_changed.connect(self.update_preview)
        self.data_manager.texts_changed.connect(self.update_preview)
        self.data_manager.current_index_changed.connect(self.on_current_index_changed)
        
        logger.info("样式设计页面初始化完成")
        
    def init_ui(self):
        """初始化界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # 左侧：样式设置
        settings_card = QFrame()
        settings_card.setObjectName("settings-card")
        settings_card.setStyleSheet("""
            QFrame#settings-card {
                background-color: white;
                border-radius: 12px;
                padding: 16px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QSpinBox, QComboBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
                min-width: 80px;
            }
            QPushButton#color-btn {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
            }
            QPushButton#center-btn {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton#center-btn:hover {
                background-color: #357abd;
            }
            QPushButton#font-btn {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                padding: 4px 8px;
                margin-left: 8px;
            }
            QPushButton#font-btn:hover {
                background-color: #357abd;
            }
        """)
        settings_layout = QVBoxLayout(settings_card)
        
        # 字体设置
        font_group = QFrame()
        font_layout = QVBoxLayout(font_group)
        font_layout.setSpacing(8)
        
        font_label = QLabel("字体设置")
        font_label.setStyleSheet("font-weight: bold;")
        font_layout.addWidget(font_label)
        
        # 添加字体选择和刷新按钮的水平布局
        font_controls = QHBoxLayout()
        self.font_combo = QComboBox()
        self.font_combo.setMinimumWidth(150)  # 增加下拉框宽度
        refresh_btn = QPushButton("刷新字体")
        refresh_btn.setObjectName("font-btn")
        refresh_btn.clicked.connect(self.refresh_fonts)
        font_controls.addWidget(QLabel("字体:"))
        font_controls.addWidget(self.font_combo)
        font_controls.addWidget(refresh_btn)
        font_layout.addLayout(font_controls)
        
        # 添加上传字体按钮
        upload_btn = QPushButton("上传字体")
        upload_btn.setObjectName("font-btn")
        upload_btn.clicked.connect(self.upload_font)
        font_layout.addWidget(upload_btn)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(self.style_config['font_size'])
        
        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("大小:"))
        size_row.addWidget(self.size_spin)
        font_layout.addLayout(size_row)
        
        self.color_btn = QPushButton("文字颜色")
        self.color_btn.setObjectName("color-btn")
        font_layout.addWidget(self.color_btn)
        
        settings_layout.addWidget(font_group)
        
        # 边距设置
        margin_group = QFrame()
        margin_layout = QVBoxLayout(margin_group)
        margin_layout.setSpacing(8)
        
        margin_label = QLabel("边距设置")
        margin_label.setStyleSheet("font-weight: bold;")
        margin_layout.addWidget(margin_label)
        
        self.margin_spins = {}
        for pos in ['top', 'bottom', 'left', 'right']:
            spin = QSpinBox()
            spin.setRange(0, 200)
            spin.setValue(self.style_config[f'margin_{pos}'])
            spin.setSuffix("px")
            
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{pos.title()}:"))
            row.addWidget(spin)
            margin_layout.addLayout(row)
            self.margin_spins[pos] = spin
        
        settings_layout.addWidget(margin_group)
        
        # 添加一键居中按钮
        center_btn = QPushButton("一键居中")
        center_btn.setObjectName("center-btn")
        center_btn.clicked.connect(self.center_text)
        settings_layout.addWidget(center_btn)
        
        # 添加批量导出按钮
        export_btn = QPushButton("批量导出")
        export_btn.setObjectName("center-btn")  # 使用相同的样式
        export_btn.clicked.connect(self.export_all)
        settings_layout.addWidget(export_btn)
        
        settings_layout.addStretch()
        
        layout.addWidget(settings_card)
        
        # 右侧：预览
        self.preview_card = PreviewCard()
        layout.addWidget(self.preview_card)
        
        # 连接信号
        self.font_combo.currentTextChanged.connect(self.on_style_changed)
        self.size_spin.valueChanged.connect(self.on_style_changed)
        self.color_btn.clicked.connect(self.select_color)
        
        for spin in self.margin_spins.values():
            spin.valueChanged.connect(self.on_margin_changed)
        
        # 修复导航按钮连接
        self.preview_card.prev_btn.clicked.connect(self.on_prev_clicked)
        self.preview_card.next_btn.clicked.connect(self.on_next_clicked)
        
        # 加载系统字体
        self.load_system_fonts()
        
        # 初始化字体设置
        self.on_style_changed()
        
    def load_system_fonts(self):
        """加载系统字体和自定义字体"""
        # 清除之前加载的自定义字体
        for font_id in self.custom_font_ids:
            QFontDatabase.removeApplicationFont(font_id)
        self.custom_font_ids.clear()
        
        # 加载自定义字体
        custom_fonts = []
        if os.path.exists(self.fonts_dir):
            for file in os.listdir(self.fonts_dir):
                if file.lower().endswith(('.ttf', '.otf')):
                    font_path = os.path.join(self.fonts_dir, file)
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        self.custom_font_ids.add(font_id)
                        font_families = QFontDatabase.applicationFontFamilies(font_id)
                        custom_fonts.extend(font_families)
                        logger.info(f"已加载自定义字体: {font_families}")
        
        # 获取系统字体
        system_fonts = QFontDatabase.families()
        
        # 合并字体列表并排序
        all_fonts = sorted(set(system_fonts + custom_fonts))
        
        # 更新字体下拉框
        current_font = self.font_combo.currentText()
        self.font_combo.clear()
        self.font_combo.addItems(all_fonts)
        
        # 恢复之前选择的字体，如果不存在则使用默认字体
        if current_font in all_fonts:
            self.font_combo.setCurrentText(current_font)
        else:
            default_font = self.style_config['font_family']
            if default_font in all_fonts:
                self.font_combo.setCurrentText(default_font)
                
    def on_style_changed(self):
        """处理样式改变"""
        logger.info("样式发生改变")
        self.style_config['font_family'] = self.font_combo.currentText()
        self.style_config['font_size'] = self.size_spin.value()
        self.update_preview()
        self.style_changed.emit()
        
    def on_margin_changed(self):
        """处理边距改变"""
        margins = {
            'top': self.margin_spins['top'].value(),
            'bottom': self.margin_spins['bottom'].value(),
            'left': self.margin_spins['left'].value(),
            'right': self.margin_spins['right'].value()
        }
        logger.info(f"边距改变: {margins}")
        for pos, value in margins.items():
            self.style_config[f'margin_{pos}'] = value
        self.update_preview()
        self.style_changed.emit()
        
    def select_color(self):
        """选择文字颜色"""
        logger.info("打开文字颜色选择器")
        color = QColorDialog.getColor(
            self.style_config['text_color'],
            self,
            "选择文字颜色"
        )
        if color.isValid():
            logger.info(f"选择了新的文字颜色: {color.name()}")
            self.style_config['text_color'] = color
            self.color_btn.setStyleSheet(
                f"background-color: {color.name()};"
                f"color: {'white' if color.lightness() < 128 else 'black'};"
            )
            self.update_preview()
            self.style_changed.emit()
            
    def center_text(self):
        """一键居中文本"""
        logger.info('点击了"一键居中"按钮')
        
        # 设置居中标志
        self.style_config['center_horizontally'] = True
        self.style_config['center_vertically'] = True
        
        # 重置边距为合理的默认值
        default_margin = 50
        for pos in ['top', 'bottom', 'left', 'right']:
            self.style_config[f'margin_{pos}'] = default_margin
            if pos in self.margin_spins:
                self.margin_spins[pos].setValue(default_margin)
        
        # 更新预览
        self.update_preview()
        self.style_changed.emit()
        self.monitor.info_occurred.emit("文本已居中")
        logger.info("完成居中操作")
        
    def on_prev_clicked(self):
        """处理上一个按钮点击"""
        logger.info('点击了"上一个"按钮')
        if self.data_manager.get_texts():
            self.data_manager.prev_text()
            self.update_preview()
        
    def on_next_clicked(self):
        """处理下一个按钮点击"""
        logger.info('点击了"下一个"按钮')
        if self.data_manager.get_texts():
            self.data_manager.next_text()
            self.update_preview()

    def update_preview(self):
        """更新预览"""
        try:
            # 获取当前图片和文本
            image_path = self.data_manager.get_image()
            text = self.data_manager.get_current_text()
            
            if not image_path or not text:
                self.preview_card.scene.clear()
                self.preview_card.view.setScene(self.preview_card.scene)
                return
            
            # 加载图片
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                logger.error("无法加载图片")
                return
            
            # 创建新场景
            self.preview_card.scene.clear()
            
            # 调整视图大小以适应图片
            view_size = self.preview_card.view.size()
            scaled_pixmap = pixmap.scaled(
                view_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # 设置场景大小并添加图片
            scene_rect = self.preview_card.scene.addPixmap(scaled_pixmap).boundingRect()
            self.preview_card.scene.setSceneRect(scene_rect)
            
            # 创建字体
            font = QFont(
                self.style_config['font_family'],
                self.style_config['font_size']
            )
            
            # 计算可用区域
            margin_left = self.style_config['margin_left']
            margin_top = self.style_config['margin_top']
            margin_right = self.style_config['margin_right']
            margin_bottom = self.style_config['margin_bottom']
            
            available_width = scaled_pixmap.width() - margin_left - margin_right
            available_height = scaled_pixmap.height() - margin_top - margin_bottom
            
            # 创建文本文档
            doc = QTextDocument()
            doc.setDefaultFont(font)
            doc.setTextWidth(available_width)
            doc.setPlainText(text)
            
            # 计算每行最大宽度
            max_line_width = 0
            for block in text.split('\n'):
                # 创建临时文档来测量实际行宽
                temp_doc = QTextDocument()
                temp_doc.setDefaultFont(font)
                temp_doc.setPlainText(block)
                line_width = temp_doc.idealWidth()
                max_line_width = max(max_line_width, line_width)
            
            # 计算文本位置（考虑整个图片尺寸）
            if self.style_config['center_horizontally']:
                # 添加额外的左侧偏移以补偿标点符号
                punctuation_compensation = font.pointSize() * 0.2  # 根据字体大小调整补偿值
                x = (scaled_pixmap.width() - max_line_width) / 2 + punctuation_compensation
            else:
                x = margin_left
            
            if self.style_config['center_vertically']:
                y = (scaled_pixmap.height() - doc.size().height()) / 2
            else:
                y = margin_top
            
            # 确保文本不会超出边距
            x = max(margin_left, min(x, scaled_pixmap.width() - margin_right - max_line_width))
            y = max(margin_top, min(y, scaled_pixmap.height() - margin_bottom - doc.size().height()))
            
            # 添加主文本
            text_item = self.preview_card.scene.addText(text, font)
            text_item.setDefaultTextColor(self.style_config['text_color'])
            text_item.setTextWidth(available_width)
            text_item.setPos(x, y)
            text_item.setZValue(1)
            
            # 设置行间距
            doc = text_item.document()
            block_format = QTextBlockFormat()
            
            # 设置行间距
            line_height = float(self.style_config['line_spacing'])
            block_format.setLineHeight(line_height, 0)  # 0 表示使用固定行高
            
            # 应用格式到所有文本块
            cursor = QTextCursor(doc)
            cursor.select(QTextCursor.Document)
            cursor.mergeBlockFormat(block_format)
            
            # 强制文档重新布局
            doc.setDefaultTextOption(text_item.document().defaultTextOption())
            doc.documentLayout().documentSizeChanged.emit(doc.size())
            
            # 更新视图
            self.preview_card.view.fitInView(
                self.preview_card.scene.sceneRect(),
                Qt.KeepAspectRatio
            )
            
            # 更新导航按钮状态
            texts = self.data_manager.get_texts()
            current_index = self.data_manager._current_index
            
            if texts:
                self.preview_card.prev_btn.setEnabled(current_index > 0)
                self.preview_card.next_btn.setEnabled(current_index < len(texts) - 1)
                logger.debug(f"更新导航按钮状态：当前索引 {current_index}，总数 {len(texts)}")
            else:
                self.preview_card.prev_btn.setEnabled(False)
                self.preview_card.next_btn.setEnabled(False)
                logger.debug("无文本，禁用导航按钮")
            
            logger.debug("预览更新成功")
            
        except Exception as e:
            logger.error(f"更新预览失败：{str(e)}")
            self.monitor.error_occurred.emit(f"更新预览失败：{str(e)}")
            
    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)
        # 更新预览以适应新大小
        self.update_preview() 

    def on_current_index_changed(self, index, total):
        """处理当前文本索引改变事件"""
        self.update_preview()
        # 更新导航按钮状态
        self.preview_card.prev_btn.setEnabled(index > 0)
        self.preview_card.next_btn.setEnabled(index < total - 1) 

    def export_all(self):
        """批量导出所有图片"""
        try:
            # 创建输出目录
            output_dir = os.path.join(os.getcwd(), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            # 为本次导出创建新的时间戳子文件夹
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = os.path.join(output_dir, f"export_{timestamp}")
            os.makedirs(export_dir, exist_ok=True)

            # 获取所有文本
            texts = self.data_manager.get_texts()
            if not texts:
                QMessageBox.warning(self, "警告", "没有可导出的内容")
                return

            # 获取原始图片
            image_path = self.data_manager.get_image()
            if not image_path:
                QMessageBox.warning(self, "警告", "请先选择背景图片")
                return

            # 创建进度对话框
            progress = QProgressDialog("正在导出图片...", "取消", 0, len(texts), self)
            progress.setWindowModality(Qt.WindowModal)
            
            # 保存当前索引
            current_index = self.data_manager._current_index
            
            # 加载原始背景图片以获取其尺寸
            original_bg = QPixmap(image_path)
            if original_bg.isNull():
                raise Exception("无法加载背景图片")
            
            # 使用原始图片的尺寸，并应用缩放因子
            scale_factor = 2  # 2倍分辨率，确保清晰度
            width = original_bg.width() * scale_factor
            height = original_bg.height() * scale_factor
            
            # 计算字体大小缩放比例
            preview_scale = self.preview_card.view.size().height() / original_bg.height()
            font_scale = 1 / preview_scale  # 反向计算实际需要的字体大小
            
            for i, text in enumerate(texts):
                if progress.wasCanceled():
                    break
                    
                # 更新进度
                progress.setValue(i)
                
                try:
                    # 创建高分辨率图像
                    image = QImage(width, height, QImage.Format_ARGB32)
                    image.fill(Qt.white)
                    
                    # 创建画笔
                    painter = QPainter()
                    if not painter.begin(image):
                        raise Exception("无法创建画笔")
                        
                    painter.setRenderHints(
                        QPainter.Antialiasing |
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform
                    )
                    
                    # 缩放以适应高分辨率
                    painter.scale(scale_factor, scale_factor)
                    
                    # 绘制背景图片（使用原始尺寸）
                    scaled_bg = original_bg.scaled(
                        original_bg.width(),
                        original_bg.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    painter.drawPixmap(0, 0, scaled_bg)
                    
                    # 创建文本文档
                    doc = QTextDocument()
                    
                    # 根据预览比例调整字体大小
                    font = QFont(self.style_config['font_family'])
                    adjusted_size = int(self.style_config['font_size'] * font_scale)
                    font.setPointSize(adjusted_size)
                    doc.setDefaultFont(font)
                    
                    # 设置文本宽度（使用原始图片尺寸计算）
                    available_width = original_bg.width() - 2 * self.style_config['margin_left']
                    doc.setTextWidth(available_width)
                    
                    # 设置文本
                    doc.setPlainText(str(text))
                    
                    # 应用文本颜色
                    cursor = QTextCursor(doc)
                    cursor.select(QTextCursor.Document)
                    format = QTextCharFormat()
                    format.setForeground(self.style_config['text_color'])
                    cursor.mergeCharFormat(format)
                    
                    # 应用行间距
                    block_format = QTextBlockFormat()
                    spacing = float(self.style_config['line_spacing'])
                    block_format.setLineHeight(int(spacing * 100), 1)  # 使用百分比行高
                    cursor.mergeBlockFormat(block_format)
                    
                    # 计算每行最大宽度
                    max_line_width = 0
                    line_count = 0
                    for block in doc.toPlainText().split('\n'):
                        # 创建临时文档来测量实际行宽
                        temp_doc = QTextDocument()
                        temp_doc.setDefaultFont(font)
                        temp_doc.setPlainText(block)
                        line_width = temp_doc.idealWidth()
                        max_line_width = max(max_line_width, line_width)
                        line_count += 1
                    
                    # 使用最大行宽来计算居中位置
                    if self.style_config['center_horizontally']:
                        # 添加较小的左侧偏移以补偿标点符号
                        punctuation_compensation = font.pointSize() * 0.1  # 减小补偿值
                        x = (original_bg.width() - max_line_width) / 2 + punctuation_compensation
                    else:
                        x = self.style_config['margin_left']
                    
                    # 优化垂直居中计算
                    text_height = doc.size().height()
                    line_height = text_height / line_count if line_count > 0 else text_height
                    
                    if self.style_config['center_vertically']:
                        # 考虑行数和行高来计算垂直居中位置
                        total_spacing = (line_count - 1) * line_height * (spacing - 1)
                        y = (original_bg.height() - text_height - total_spacing) / 2
                    else:
                        y = self.style_config['margin_top']
                    
                    # 绘制文本
                    painter.save()
                    painter.translate(x, y)
                    doc.drawContents(painter)
                    painter.restore()
                    
                    # 确保正确结束绘制
                    painter.end()
                    
                    # 保存图片
                    output_path = os.path.join(export_dir, f"导出图片_{i+1}.png")
                    success = image.save(output_path, "PNG", quality=100)
                    
                    if not success:
                        raise Exception(f"保存图片 {i+1} 失败")
                    
                except Exception as e:
                    logger.error(f"导出图片 {i+1} 失败: {str(e)}")
                    continue
            
            # 恢复之前的索引
            self.data_manager._current_index = current_index
            
            progress.setValue(len(texts))
            QMessageBox.information(self, "完成", f"图片已导出到:\n{export_dir}")
            
        except Exception as e:
            logger.error(f"导出失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}") 

    def refresh_fonts(self):
        """刷新字体列表"""
        logger.info("刷新字体列表")
        self.load_system_fonts()
        self.monitor.info_occurred.emit("字体列表已刷新")
        
    def upload_font(self):
        """上传字体文件"""
        logger.info("打开字体文件选择对话框")
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("字体文件 (*.ttf *.otf)")
        file_dialog.setWindowTitle("选择字体文件")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            success_count = 0
            
            for file_path in selected_files:
                try:
                    # 获取文件名
                    file_name = os.path.basename(file_path)
                    # 构建目标路径
                    target_path = os.path.join(self.fonts_dir, file_name)
                    
                    # 复制字体文件到字体目录
                    import shutil
                    shutil.copy2(file_path, target_path)
                    success_count += 1
                    logger.info(f"成功复制字体文件: {file_name}")
                    
                except Exception as e:
                    logger.error(f"复制字体文件失败: {str(e)}")
                    continue
            
            if success_count > 0:
                # 刷新字体列表
                self.refresh_fonts()
                self.monitor.info_occurred.emit(f"成功添加 {success_count} 个字体文件")
            else:
                self.monitor.error_occurred.emit("没有字体文件被添加") 