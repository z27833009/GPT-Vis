"""
测试包初始化文件

包含公共的测试配置和导入
"""

import os
import sys

# 添加父目录到 Python 路径，以便导入被测试的模块
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from jsonschema import ValidationError
    from validate import validate_params, validate_tree_data, validate_node_edge_data
except ImportError as e:
    print(f"导入错误: {e}")
    print("请安装依赖: pip install pytest jsonschema")
    sys.exit(1)

__all__ = [
    'ValidationError',
    'validate_params', 
    'validate_tree_data', 
    'validate_node_edge_data'
]
