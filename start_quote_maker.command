#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到程序目录
cd "$SCRIPT_DIR"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查必要的包是否安装
echo "正在检查环境..."
python3 -m pip install -q PySide6 openpyxl markdown pandas || {
    echo "错误：安装依赖包失败"
    exit 1
}

# 创建fonts和docs目录（如果不存在）
mkdir -p fonts docs

# 启动程序
echo "正在启动 Quote Maker..."
python3 main.py 