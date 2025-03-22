# Quote Maker - 图文生成器

一个简单易用的图文生成工具，支持从 Excel 导入文本并生成精美的图片。

## 功能特点

- 支持从 Excel 导入文本
- 支持自定义字体和样式
- 支持批量导出图片
- 简单直观的用户界面

## 使用方法

1. 双击 `start_quote_maker.command` 启动程序
2. 导入 Excel 文件或直接输入文本
3. 设置字体、颜色、大小等样式
4. 点击导出即可生成图片

## 系统要求

- macOS 系统
- Python 3.x
- 必要的 Python 包（会自动安装）：
  - PySide6
  - openpyxl
  - markdown

## 目录结构

- `start_quote_maker.command`: 启动脚本
- `main.py`: 主程序
- `ui/`: 界面相关代码
- `core/`: 核心功能代码
- `docs/`: 帮助文档
- `fonts/`: 字体文件夹

## 注意事项

- 首次运行时可能需要在系统偏好设置中允许运行
- 请不要移动或删除程序目录中的文件
- 如遇问题，请查看 logs 文件夹中的日志 