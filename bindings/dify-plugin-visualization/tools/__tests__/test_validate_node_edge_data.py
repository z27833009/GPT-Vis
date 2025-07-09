"""
测试 validate_node_edge_data 函数

该文件专门测试 validate.py 中的 validate_node_edge_data 函数
包含正向测试和负向测试用例

运行测试：
pytest __tests__/test_validate_node_edge_data.py -v
"""

import pytest
from . import ValidationError, validate_node_edge_data
from .conftest import (
    VALID_NODE_EDGE_DATA,
    COMPLEX_GRAPH_DATA,
    assert_no_exception,
    create_node_edge_data_variants
)


class TestValidateNodeEdgeDataPositive:
    """测试 validate_node_edge_data 函数的正向用例"""
    
    def test_valid_node_edge_data(self, valid_graph_data):
        """测试有效的节点边数据"""
        result = assert_no_exception(validate_node_edge_data, valid_graph_data)
        assert result is True
    
    def test_empty_nodes_and_edges(self):
        """测试空的节点和边数据"""
        empty_data = {
            "nodes": [],
            "edges": []
        }
        result = assert_no_exception(validate_node_edge_data, empty_data)
        assert result is True
    
    def test_nodes_only_no_edges(self):
        """测试只有节点没有边的情况"""
        nodes_only = {
            "nodes": [
                {"name": "A"},
                {"name": "B"},
                {"name": "C"}
            ],
            "edges": []
        }
        result = assert_no_exception(validate_node_edge_data, nodes_only)
        assert result is True
    
    def test_single_node_no_edges(self):
        """测试单个节点无边的情况"""
        single_node = {
            "nodes": [{"name": "lonely_node"}],
            "edges": []
        }
        result = assert_no_exception(validate_node_edge_data, single_node)
        assert result is True
    
    def test_complex_valid_graph(self):
        """测试复杂的有效图数据"""
        result = assert_no_exception(validate_node_edge_data, COMPLEX_GRAPH_DATA)
        assert result is True
    
    def test_fully_connected_graph(self):
        """测试全连接图"""
        fully_connected = {
            "nodes": [
                {"name": "A"},
                {"name": "B"},
                {"name": "C"}
            ],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "A", "target": "C"},
                {"source": "B", "target": "A"},
                {"source": "B", "target": "C"},
                {"source": "C", "target": "A"},
                {"source": "C", "target": "B"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, fully_connected)
        assert result is True
    
    def test_self_loop_allowed(self):
        """测试自环边（节点指向自己）"""
        self_loop_graph = {
            "nodes": [
                {"name": "A"},
                {"name": "B"}
            ],
            "edges": [
                {"source": "A", "target": "A"},  # 自环
                {"source": "A", "target": "B"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, self_loop_graph)
        assert result is True
    
    def test_nodes_with_additional_properties(self):
        """测试包含额外属性的节点"""
        nodes_with_props = {
            "nodes": [
                {"name": "A", "value": 100, "type": "input"},
                {"name": "B", "value": 200, "type": "process"},
                {"name": "C", "value": 300, "type": "output"}
            ],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "B", "target": "C"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, nodes_with_props)
        assert result is True
    
    def test_edges_with_additional_properties(self):
        """测试包含额外属性的边"""
        edges_with_props = {
            "nodes": [
                {"name": "A"},
                {"name": "B"},
                {"name": "C"}
            ],
            "edges": [
                {"source": "A", "target": "B", "weight": 10, "type": "strong"},
                {"source": "B", "target": "C", "weight": 5, "type": "weak"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, edges_with_props)
        assert result is True


class TestValidateNodeEdgeDataNegative:
    """测试 validate_node_edge_data 函数的负向用例"""
    
    def test_missing_node_name(self):
        """测试缺少节点名称"""
        invalid_data = {
            "nodes": [
                {"name": "A"},
                {}  # 缺少 name 字段
            ],
            "edges": []
        }
        
        with pytest.raises(ValidationError, match="node name is missing"):
            validate_node_edge_data(invalid_data)
    
    def test_node_name_is_none(self):
        """测试节点名称为 None"""
        invalid_data = {
            "nodes": [
                {"name": "A"},
                {"name": None}  # name 为 None
            ],
            "edges": []
        }
        
        with pytest.raises(ValidationError, match="node name is missing"):
            validate_node_edge_data(invalid_data)
    
    def test_duplicate_node_names(self):
        """测试重复的节点名称"""
        invalid_data = {
            "nodes": [
                {"name": "A"},
                {"name": "B"},
                {"name": "A"}  # 重复名称
            ],
            "edges": []
        }
        
        with pytest.raises(ValidationError, match="nodes name 'A' is not unique"):
            validate_node_edge_data(invalid_data)
    
    def test_missing_edge_source(self):
        """测试缺少边的源节点"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"target": "B"}  # 缺少 source
            ]
        }
        
        with pytest.raises(ValidationError, match="edge source or target is missing"):
            validate_node_edge_data(invalid_data)
    
    def test_missing_edge_target(self):
        """测试缺少边的目标节点"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"source": "A"}  # 缺少 target
            ]
        }
        
        with pytest.raises(ValidationError, match="edge source or target is missing"):
            validate_node_edge_data(invalid_data)
    
    def test_edge_source_not_in_nodes(self):
        """测试边的源节点不存在于节点列表中"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"source": "C", "target": "A"}  # C 不存在于节点中
            ]
        }
        
        with pytest.raises(ValidationError, match="source 'C' does not exist in nodes"):
            validate_node_edge_data(invalid_data)
    
    def test_edge_target_not_in_nodes(self):
        """测试边的目标节点不存在于节点列表中"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"source": "A", "target": "C"}  # C 不存在于节点中
            ]
        }
        
        with pytest.raises(ValidationError, match="target 'C' does not exist in nodes"):
            validate_node_edge_data(invalid_data)
    
    def test_duplicate_edge_pairs(self):
        """测试重复的边对"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "A", "target": "B"}  # 重复的边
            ]
        }
        
        with pytest.raises(ValidationError, match="edge pair 'A-B' is not unique"):
            validate_node_edge_data(invalid_data)
    
    def test_both_source_and_target_missing(self):
        """测试边的源和目标都缺少"""
        invalid_data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {}  # 既没有 source 也没有 target
            ]
        }
        
        with pytest.raises(ValidationError, match="edge source or target is missing"):
            validate_node_edge_data(invalid_data)
    
    @pytest.mark.parametrize("invalid_data", [
        # 缺少节点名称
        {"nodes": [{"name": "A"}, {}], "edges": []},
        # 重复节点名称
        {"nodes": [{"name": "A"}, {"name": "A"}], "edges": []},
        # 边的源不存在
        {"nodes": [{"name": "A"}], "edges": [{"source": "B", "target": "A"}]},
        # 边的目标不存在
        {"nodes": [{"name": "A"}], "edges": [{"source": "A", "target": "B"}]},
        # 重复边
        {"nodes": [{"name": "A"}, {"name": "B"}], "edges": [{"source": "A", "target": "B"}, {"source": "A", "target": "B"}]},
    ])
    def test_various_invalid_data(self, invalid_data):
        """参数化测试各种无效数据"""
        with pytest.raises(ValidationError):
            validate_node_edge_data(invalid_data)


class TestValidateNodeEdgeDataEdgeCases:
    """测试 validate_node_edge_data 函数的边界情况"""
    
    def test_empty_string_node_names(self):
        """测试空字符串节点名称"""
        data_with_empty_names = {
            "nodes": [
                {"name": ""},  # 空字符串
                {"name": "B"}
            ],
            "edges": [
                {"source": "", "target": "B"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, data_with_empty_names)
        assert result is True
    
    def test_numeric_node_names(self):
        """测试数字节点名称"""
        numeric_nodes = {
            "nodes": [
                {"name": "1"},
                {"name": "2"},
                {"name": "3"}
            ],
            "edges": [
                {"source": "1", "target": "2"},
                {"source": "2", "target": "3"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, numeric_nodes)
        assert result is True
    
    def test_unicode_node_names(self):
        """测试 Unicode 字符节点名称"""
        unicode_nodes = {
            "nodes": [
                {"name": "节点A"},
                {"name": "节点B"},
                {"name": "节点🌟"}
            ],
            "edges": [
                {"source": "节点A", "target": "节点B"},
                {"source": "节点B", "target": "节点🌟"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, unicode_nodes)
        assert result is True
    
    def test_special_character_node_names(self):
        """测试特殊字符节点名称"""
        special_char_nodes = {
            "nodes": [
                {"name": "node@#$"},
                {"name": "node!@#"},
                {"name": "node%^&"}
            ],
            "edges": [
                {"source": "node@#$", "target": "node!@#"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, special_char_nodes)
        assert result is True
    
    def test_very_long_node_names(self):
        """测试很长的节点名称"""
        long_name = "a" * 1000
        long_name_nodes = {
            "nodes": [
                {"name": long_name},
                {"name": "short"}
            ],
            "edges": [
                {"source": long_name, "target": "short"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, long_name_nodes)
        assert result is True
    
    def test_whitespace_node_names(self):
        """测试包含空白字符的节点名称"""
        whitespace_nodes = {
            "nodes": [
                {"name": " node A "},
                {"name": "\tnode B\t"},
                {"name": "\nnode C\n"}
            ],
            "edges": [
                {"source": " node A ", "target": "\tnode B\t"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, whitespace_nodes)
        assert result is True
    
    def test_large_graph(self):
        """测试大型图（性能测试）"""
        # 创建包含 100 个节点的图
        large_graph = {
            "nodes": [{"name": f"node_{i}"} for i in range(100)],
            "edges": [
                {"source": f"node_{i}", "target": f"node_{(i+1) % 100}"}
                for i in range(100)
            ]
        }
        result = assert_no_exception(validate_node_edge_data, large_graph)
        assert result is True
    
    def test_missing_nodes_key(self):
        """测试缺少 nodes 键的情况"""
        data_without_nodes = {
            "edges": []  # 没有边，所以应该通过
        }
        # 这应该通过，因为空的节点列表和边列表是有效的
        result = assert_no_exception(validate_node_edge_data, data_without_nodes)
        assert result is True
    
    def test_missing_edges_key(self):
        """测试缺少 edges 键的情况"""
        data_without_edges = {
            "nodes": [{"name": "A"}, {"name": "B"}]
        }
        result = assert_no_exception(validate_node_edge_data, data_without_edges)
        assert result is True


class TestValidateNodeEdgeDataComplexScenarios:
    """测试 validate_node_edge_data 函数的复杂场景"""
    
    def test_social_network(self):
        """测试社交网络场景"""
        social_network = {
            "nodes": [
                {"name": "Alice", "followers": 100},
                {"name": "Bob", "followers": 50},
                {"name": "Charlie", "followers": 200},
                {"name": "David", "followers": 75}
            ],
            "edges": [
                {"source": "Alice", "target": "Bob", "relationship": "follows"},
                {"source": "Bob", "target": "Charlie", "relationship": "follows"},
                {"source": "Charlie", "target": "Alice", "relationship": "follows"},
                {"source": "David", "target": "Alice", "relationship": "follows"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, social_network)
        assert result is True
    
    def test_workflow_graph(self):
        """测试工作流图场景"""
        workflow = {
            "nodes": [
                {"name": "开始", "type": "start"},
                {"name": "数据输入", "type": "input"},
                {"name": "数据处理", "type": "process"},
                {"name": "数据验证", "type": "validation"},
                {"name": "数据输出", "type": "output"},
                {"name": "结束", "type": "end"}
            ],
            "edges": [
                {"source": "开始", "target": "数据输入"},
                {"source": "数据输入", "target": "数据处理"},
                {"source": "数据处理", "target": "数据验证"},
                {"source": "数据验证", "target": "数据输出"},
                {"source": "数据输出", "target": "结束"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, workflow)
        assert result is True
    
    def test_dependency_graph(self):
        """测试依赖关系图场景"""
        dependencies = {
            "nodes": [
                {"name": "模块A", "version": "1.0"},
                {"name": "模块B", "version": "2.1"},
                {"name": "模块C", "version": "1.5"},
                {"name": "模块D", "version": "3.0"}
            ],
            "edges": [
                {"source": "模块A", "target": "模块B", "type": "depends_on"},
                {"source": "模块A", "target": "模块C", "type": "depends_on"},
                {"source": "模块B", "target": "模块D", "type": "depends_on"},
                {"source": "模块C", "target": "模块D", "type": "depends_on"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, dependencies)
        assert result is True
    
    def test_network_topology(self):
        """测试网络拓扑场景"""
        network = {
            "nodes": [
                {"name": "路由器1", "ip": "192.168.1.1"},
                {"name": "路由器2", "ip": "192.168.1.2"},
                {"name": "交换机1", "ip": "192.168.1.10"},
                {"name": "交换机2", "ip": "192.168.1.11"},
                {"name": "服务器1", "ip": "192.168.1.100"},
                {"name": "服务器2", "ip": "192.168.1.101"}
            ],
            "edges": [
                {"source": "路由器1", "target": "交换机1", "bandwidth": "1Gbps"},
                {"source": "路由器2", "target": "交换机2", "bandwidth": "1Gbps"},
                {"source": "交换机1", "target": "服务器1", "bandwidth": "100Mbps"},
                {"source": "交换机2", "target": "服务器2", "bandwidth": "100Mbps"},
                {"source": "路由器1", "target": "路由器2", "bandwidth": "10Gbps"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, network)
        assert result is True
    
    def test_decision_tree(self):
        """测试决策树场景"""
        decision_tree = {
            "nodes": [
                {"name": "根决策", "type": "decision"},
                {"name": "条件A", "type": "condition"},
                {"name": "条件B", "type": "condition"},
                {"name": "结果1", "type": "result"},
                {"name": "结果2", "type": "result"},
                {"name": "结果3", "type": "result"}
            ],
            "edges": [
                {"source": "根决策", "target": "条件A", "condition": "if_true"},
                {"source": "根决策", "target": "条件B", "condition": "if_false"},
                {"source": "条件A", "target": "结果1", "condition": "if_true"},
                {"source": "条件A", "target": "结果2", "condition": "if_false"},
                {"source": "条件B", "target": "结果3", "condition": "always"}
            ]
        }
        result = assert_no_exception(validate_node_edge_data, decision_tree)
        assert result is True
