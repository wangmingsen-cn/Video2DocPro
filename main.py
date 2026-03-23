#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py — Video2Doc Pro 入口文件
用法：python main.py
或双击 Video2DocPro.exe（打包后）
"""

import sys, os

# 添加 src 目录到 Python 路径
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SRC_DIR, "src"))

if __name__ == "__main__":
    from src.app import main
    main()
