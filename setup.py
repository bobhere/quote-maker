"""
打包脚本
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('', ['docs']),  # 包含整个 docs 目录
    ('', ['fonts']), # 包含整个 fonts 目录
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PySide6', 'openpyxl', 'markdown'],
    'plist': {
        'CFBundleName': 'Quote Maker',
        'CFBundleDisplayName': 'Quote Maker',
        'CFBundleIdentifier': 'com.quotemaker.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2024',
    }
}

setup(
    name='Quote Maker',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 