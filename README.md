# Quote Maker (图文生成器)

一个优雅的图文处理工具，用于制作适合社交媒体分享的图文内容。

## 功能特点

- 支持中英文对照排版
- 丰富的字体和样式选项
- 直观的用户界面
- 实时预览效果
- 高质量图片输出

## 系统要求

- Python 3.8+
- 操作系统：Windows/macOS/Linux

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/quote-maker.git
cd quote-maker
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python main.py
```

## 使用说明

1. 导入文本：支持Excel文件导入，包含中英文对照
2. 选择背景：支持JPG、PNG、BMP格式图片
3. 调整样式：字体、大小、颜色、位置等
4. 生成图片：保存为高质量图片文件

## 开发说明

- 使用PySide6构建GUI
- 使用Pillow处理图片
- 使用pandas处理Excel数据

## 许可证

MIT License 