"""
测试 validate_tree_data 函数

该文件专门测试 validate.py 中的 validate_tree_data 函数
包含正向测试和负向测试用例

运行测试：
pytest __tests__/test_validate_tree_data.py -v
"""

import pytest
from . import ValidationError, validate_tree_data
from .conftest import (
    VALID_TREE_DATA,
    assert_no_exception,
    create_tree_data_variants
)


class TestValidateTreeDataPositive:
    """测试 validate_tree_data 函数的正向用例"""
    
    def test_valid_tree_data(self, valid_tree_data):
        """测试有效的多层树形数据"""
        result = assert_no_exception(validate_tree_data, valid_tree_data)
        assert result is True
    
    def test_simple_valid_tree(self):
        """测试简单的单节点树"""
        simple_tree = {"name": "single_node"}
        result = assert_no_exception(validate_tree_data, simple_tree)
        assert result is True
    
    def test_tree_with_empty_children(self):
        """测试包含空 children 列表的树"""
        tree_with_empty_children = {
            "name": "root",
            "children": []
        }
        result = assert_no_exception(validate_tree_data, tree_with_empty_children)
        assert result is True
    
    def test_deep_nested_tree(self):
        """测试深度嵌套的树形结构"""
        deep_tree = {
            "name": "level0",
            "children": [{
                "name": "level1",
                "children": [{
                    "name": "level2",
                    "children": [{
                        "name": "level3",
                        "children": [{
                            "name": "level4"
                        }]
                    }]
                }]
            }]
        }
        result = assert_no_exception(validate_tree_data, deep_tree)
        assert result is True
    
    def test_wide_tree_structure(self):
        """测试宽树形结构（许多兄弟节点）"""
        wide_tree = {
            "name": "root",
            "children": [
                {"name": f"child_{i}"} for i in range(10)
            ]
        }
        result = assert_no_exception(validate_tree_data, wide_tree)
        assert result is True
    
    def test_mixed_tree_structure(self):
        """测试混合结构（有些节点有子节点，有些没有）"""
        mixed_tree = {
            "name": "root",
            "children": [
                {
                    "name": "branch_node",
                    "children": [
                        {"name": "leaf1"},
                        {"name": "leaf2"}
                    ]
                },
                {"name": "leaf_node"},  # 没有 children
                {
                    "name": "another_branch",
                    "children": [{"name": "another_leaf"}]
                }
            ]
        }
        result = assert_no_exception(validate_tree_data, mixed_tree)
        assert result is True
    
    def test_tree_with_additional_properties(self):
        """测试包含额外属性的树节点"""
        tree_with_props = {
            "name": "root",
            "value": 100,  # 额外属性
            "type": "folder",  # 额外属性
            "children": [
                {
                    "name": "child1",
                    "value": 50,
                    "type": "file"
                },
                {
                    "name": "child2",
                    "value": 30,
                    "type": "folder",
                    "children": [
                        {
                            "name": "grandchild",
                            "value": 20,
                            "type": "file"
                        }
                    ]
                }
            ]
        }
        result = assert_no_exception(validate_tree_data, tree_with_props)
        assert result is True


class TestValidateTreeDataNegative:
    """测试 validate_tree_data 函数的负向用例"""
    
    def test_missing_root_name(self):
        """测试缺少根节点名称"""
        invalid_tree = {
            "children": [{"name": "child1"}]
        }
        
        with pytest.raises(ValidationError, match="root node name is missing"):
            validate_tree_data(invalid_tree)
    
    def test_root_name_is_none(self):
        """测试根节点名称为 None"""
        invalid_tree = {
            "name": None,
            "children": [{"name": "child1"}]
        }
        
        with pytest.raises(ValidationError, match="root node name is missing"):
            validate_tree_data(invalid_tree)
    
    def test_missing_child_name(self):
        """测试缺少子节点名称"""
        invalid_tree = {
            "name": "root",
            "children": [
                {"name": "child1"},
                {}  # 缺少 name 字段
            ]
        }
        
        with pytest.raises(ValidationError, match="node name is missing"):
            validate_tree_data(invalid_tree)
    
    def test_child_name_is_none(self):
        """测试子节点名称为 None"""
        invalid_tree = {
            "name": "root",
            "children": [
                {"name": "child1"},
                {"name": None}  # name 为 None
            ]
        }
        
        with pytest.raises(ValidationError, match="node name is missing"):
            validate_tree_data(invalid_tree)
    
    def test_duplicate_child_names(self):
        """测试同级节点重复名称"""
        invalid_tree = {
            "name": "root",
            "children": [
                {"name": "duplicate"},
                {"name": "unique"},
                {"name": "duplicate"}  # 重复名称
            ]
        }
        
        with pytest.raises(ValidationError, match="node name 'duplicate' is not unique"):
            validate_tree_data(invalid_tree)
    
    def test_duplicate_names_across_levels(self):
        """测试跨层级的重复节点名称"""
        invalid_tree = {
            "name": "root",
            "children": [
                {
                    "name": "child1",
                    "children": [
                        {"name": "root"}  # 与根节点同名
                    ]
                }
            ]
        }
        
        with pytest.raises(ValidationError, match="node name 'root' is not unique"):
            validate_tree_data(invalid_tree)
    
    def test_duplicate_names_deep_nesting(self):
        """测试深度嵌套中的重复名称"""
        invalid_tree = {
            "name": "root",
            "children": [{
                "name": "level1",
                "children": [{
                    "name": "level2",
                    "children": [{
                        "name": "level1"  # 与上级节点重复
                    }]
                }]
            }]
        }
        
        with pytest.raises(ValidationError, match="node name 'level1' is not unique"):
            validate_tree_data(invalid_tree)
    
    def test_duplicate_names_in_different_branches(self):
        """测试不同分支中的重复名称"""
        invalid_tree = {
            "name": "root",
            "children": [
                {
                    "name": "branch1",
                    "children": [{"name": "common_name"}]
                },
                {
                    "name": "branch2",
                    "children": [{"name": "common_name"}]  # 重复名称
                }
            ]
        }
        
        with pytest.raises(ValidationError, match="node name 'common_name' is not unique"):
            validate_tree_data(invalid_tree)
    
    @pytest.mark.parametrize("invalid_tree_data", [
        {"children": [{"name": "child"}]},  # 缺少根名称
        {"name": "root", "children": [{}]},  # 子节点缺少名称
        {"name": "root", "children": [{"name": "dup"}, {"name": "dup"}]},  # 重复名称
    ])
    def test_various_invalid_trees(self, invalid_tree_data):
        """参数化测试各种无效树形数据"""
        with pytest.raises(ValidationError):
            validate_tree_data(invalid_tree_data)


class TestValidateTreeDataEdgeCases:
    """测试 validate_tree_data 函数的边界情况"""
    
    def test_empty_tree(self):
        """测试空树（只有根节点名称）"""
        empty_tree = {"name": "empty_root"}
        result = assert_no_exception(validate_tree_data, empty_tree)
        assert result is True
    
    def test_tree_with_empty_string_names(self):
        """测试包含空字符串名称的树"""
        tree_with_empty_names = {
            "name": "",  # 空字符串名称
            "children": [
                {"name": "child1"},
                {"name": ""}  # 空字符串名称
            ]
        }
        
        # 空字符串名称可能被认为是有效的，但会导致重复
        with pytest.raises(ValidationError, match="is not unique"):
            validate_tree_data(tree_with_empty_names)
    
    def test_tree_with_numeric_names(self):
        """测试包含数字名称的树"""
        numeric_tree = {
            "name": "123",
            "children": [
                {"name": "456"},
                {"name": "789"}
            ]
        }
        result = assert_no_exception(validate_tree_data, numeric_tree)
        assert result is True
    
    def test_tree_with_special_character_names(self):
        """测试包含特殊字符名称的树"""
        special_char_tree = {
            "name": "root@#$%",
            "children": [
                {"name": "child_!@#"},
                {"name": "child_$%^"}
            ]
        }
        result = assert_no_exception(validate_tree_data, special_char_tree)
        assert result is True
    
    def test_tree_with_unicode_names(self):
        """测试包含 Unicode 字符名称的树"""
        unicode_tree = {
            "name": "根节点",
            "children": [
                {"name": "子节点1"},
                {"name": "子节点2"},
                {
                    "name": "子节点3",
                    "children": [
                        {"name": "孙节点📁"},
                        {"name": "孙节点🌟"}
                    ]
                }
            ]
        }
        result = assert_no_exception(validate_tree_data, unicode_tree)
        assert result is True
    
    def test_tree_with_very_long_names(self):
        """测试包含很长名称的树"""
        long_name = "a" * 1000  # 1000 个字符的名称
        long_name_tree = {
            "name": "root",
            "children": [
                {"name": long_name},
                {"name": "short"}
            ]
        }
        result = assert_no_exception(validate_tree_data, long_name_tree)
        assert result is True
    
    def test_tree_with_whitespace_names(self):
        """测试包含空白字符名称的树"""
        whitespace_tree = {
            "name": " root ",
            "children": [
                {"name": "\tchild1\t"},
                {"name": "\nchild2\n"},
                {"name": "  spaced  child  "}
            ]
        }
        result = assert_no_exception(validate_tree_data, whitespace_tree)
        assert result is True
    
    def test_maximum_depth_tree(self):
        """测试最大深度的树（防止栈溢出）"""
        # 创建一个深度为 100 的树
        current = {"name": "leaf100"}
        for i in range(99, -1, -1):
            current = {
                "name": f"node{i}",
                "children": [current]
            }
        
        result = assert_no_exception(validate_tree_data, current)
        assert result is True


class TestValidateTreeDataComplexScenarios:
    """测试 validate_tree_data 函数的复杂场景"""
    
    def test_organizational_chart(self):
        """测试组织架构图场景"""
        org_chart = {
            "name": "CEO",
            "children": [
                {
                    "name": "CTO",
                    "children": [
                        {"name": "前端组长"},
                        {"name": "后端组长"},
                        {"name": "测试组长"}
                    ]
                },
                {
                    "name": "CMO",
                    "children": [
                        {"name": "市场专员"},
                        {"name": "品牌专员"}
                    ]
                },
                {"name": "CFO"}
            ]
        }
        result = assert_no_exception(validate_tree_data, org_chart)
        assert result is True
    
    def test_file_system_structure(self):
        """测试文件系统结构场景"""
        file_system = {
            "name": "root",
            "children": [
                {
                    "name": "home",
                    "children": [
                        {
                            "name": "user",
                            "children": [
                                {"name": "documents"},
                                {"name": "downloads"},
                                {"name": "pictures"}
                            ]
                        }
                    ]
                },
                {
                    "name": "var",
                    "children": [
                        {"name": "log"},
                        {"name": "cache"}
                    ]
                },
                {"name": "etc"}
            ]
        }
        result = assert_no_exception(validate_tree_data, file_system)
        assert result is True
    
    def test_menu_structure(self):
        """测试菜单结构场景"""
        menu_structure = {
            "name": "主菜单",
            "children": [
                {
                    "name": "文件",
                    "children": [
                        {"name": "新建"},
                        {"name": "打开"},
                        {"name": "保存"},
                        {
                            "name": "最近文件",
                            "children": [
                                {"name": "文档1.txt"},
                                {"name": "文档2.txt"}
                            ]
                        }
                    ]
                },
                {
                    "name": "编辑",
                    "children": [
                        {"name": "复制"},
                        {"name": "粘贴"},
                        {"name": "撤销"}
                    ]
                },
                {"name": "帮助"}
            ]
        }
        result = assert_no_exception(validate_tree_data, menu_structure)
        assert result is True
