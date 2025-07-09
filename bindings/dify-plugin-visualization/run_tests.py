#!/usr/bin/env python3
"""
在 dify-plugin-visualization 根目录运行 validate.py 测试套件

使用方法:
python run_validate_tests.py [选项]

选项:
--verbose, -v    详细输出
--quick, -q      快速运行（只显示结果）
--coverage       生成覆盖率报告
--summary        只显示测试统计
--help, -h       显示帮助信息
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def find_tools_dir():
    """查找 tools 目录"""
    current_dir = Path(__file__).parent
    tools_dir = current_dir / "tools"
    
    if not tools_dir.exists():
        print("❌ 未找到 tools 目录")
        print(f"当前目录: {current_dir}")
        print("请确保在 dify-plugin-visualization 根目录运行此脚本")
        return None
    
    return tools_dir

def check_test_structure(tools_dir):
    """检查测试结构是否完整"""
    required_files = [
        "validate.py",
        "__tests__/__init__.py",
        "__tests__/conftest.py",
        "__tests__/test_validate_params.py",
        "__tests__/test_validate_tree_data.py",
        "__tests__/test_validate_node_edge_data.py",
        "__tests__/test_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (tools_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下测试文件:")
        for file in missing_files:
            print(f"   {file}")
        return False
    
    return True

def get_test_statistics(tools_dir):
    """获取测试统计信息"""
    test_files = [
        "__tests__/test_validate_params.py",
        "__tests__/test_validate_tree_data.py", 
        "__tests__/test_validate_node_edge_data.py",
        "__tests__/test_integration.py"
    ]
    
    stats = {}
    total_tests = 0
    total_classes = 0
    
    for test_file in test_files:
        file_path = tools_dir / test_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_count = content.count('def test_')
                    class_count = content.count('class Test')
                    
                    stats[os.path.basename(test_file)] = {
                        'tests': test_count,
                        'classes': class_count
                    }
                    total_tests += test_count
                    total_classes += class_count
            except Exception as e:
                print(f"⚠️  读取 {test_file} 时出错: {e}")
    
    return stats, total_tests, total_classes

def check_dependencies():
    """检查测试依赖"""
    try:
        import pytest
        import jsonschema
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install pytest jsonschema")
        return False

def run_tests(tools_dir, verbose=False, quick=False, coverage=False):
    """运行测试"""
    # 构建命令
    cmd = [sys.executable, '-m', 'pytest', 'tools/__tests__/']
    
    if verbose:
        cmd.append('-v')
    elif quick:
        cmd.append('-q')
    else:
        cmd.extend(['-v', '--tb=short'])
    
    if coverage:
        cmd.extend(['--cov=tools/validate', '--cov-report=term-missing'])
    
    print(f"运行命令: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # 改变工作目录到 dify-plugin-visualization 根目录
        original_cwd = os.getcwd()
        os.chdir(tools_dir.parent)
        
        result = subprocess.run(cmd, check=False)
        
        # 恢复原始工作目录
        os.chdir(original_cwd)
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return False
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print(__doc__)
    print("\n示例:")
    print("  python run_validate_tests.py              # 运行所有测试")
    print("  python run_validate_tests.py -v           # 详细输出")
    print("  python run_validate_tests.py -q           # 快速运行")
    print("  python run_validate_tests.py --coverage   # 生成覆盖率")
    print("  python run_validate_tests.py --summary    # 只显示统计")

def main():
    parser = argparse.ArgumentParser(description='运行 validate.py 测试套件')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('-q', '--quick', action='store_true', help='快速运行')
    parser.add_argument('--coverage', action='store_true', help='生成覆盖率报告')
    parser.add_argument('--summary', action='store_true', help='只显示测试统计')
    
    args = parser.parse_args()
    
    if args.verbose and args.quick:
        print("❌ --verbose 和 --quick 选项不能同时使用")
        return False
    
    print("🧪 validate.py 测试套件")
    print("=" * 60)
    print(f"工作目录: {os.getcwd()}")
    
    # 查找 tools 目录
    tools_dir = find_tools_dir()
    if not tools_dir:
        return False
    
    print(f"测试目录: {tools_dir}")
    
    # 检查测试结构
    if not check_test_structure(tools_dir):
        return False
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    # 获取并显示测试统计
    stats, total_tests, total_classes = get_test_statistics(tools_dir)
    
    print("\n📊 测试文件统计:")
    for filename, info in stats.items():
        print(f"  📁 {filename}: {info['classes']} 类, {info['tests']} 测试")
    
    print(f"\n总计: {total_classes} 个测试类, {total_tests} 个测试方法")
    
    if args.summary:
        return True
    
    # 运行测试
    print("\n🚀 运行所有测试...")
    success = run_tests(tools_dir, args.verbose, args.quick, args.coverage)
    
    if success:
        print("\n✅ 所有测试通过!")
        if args.coverage:
            print("📊 覆盖率报告已生成")
    else:
        print("\n❌ 部分测试失败")
    
    return success

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 运行时出错: {e}")
        sys.exit(1)
