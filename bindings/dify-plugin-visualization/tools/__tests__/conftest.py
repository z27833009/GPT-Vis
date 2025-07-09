"""
测试工具和固定装置 (Test Fixtures)

包含测试中使用的公共数据和工具函数
"""

import pytest

# 公共测试数据
VALID_AREA_CHART_DATA = {
    "data": [
        {"time": "2018", "value": 99.9},
        {"time": "2019", "value": 120.5},
        {"time": "2020", "value": 88.2}
    ],
    "width": 600,
    "height": 400,
    "title": "测试面积图",
    "theme": "default"
}

VALID_STACKED_AREA_DATA = {
    "data": [
        {"time": "2018", "value": 99.9, "group": "A"},
        {"time": "2018", "value": 120.5, "group": "B"},
        {"time": "2019", "value": 88.2, "group": "A"},
        {"time": "2019", "value": 95.1, "group": "B"}
    ],
    "stack": True,
    "width": 800,
    "height": 500
}

VALID_BAR_CHART_DATA = {
    "data": [
        {"category": "A", "value": 100},
        {"category": "B", "value": 200},
        {"category": "C", "value": 150}
    ]
}

VALID_PIE_CHART_DATA = {
    "data": [
        {"category": "类别A", "value": 100},
        {"category": "类别B", "value": 200},
        {"category": "类别C", "value": 150}
    ]
}

VALID_TREE_DATA = {
    "name": "root",
    "children": [
        {
            "name": "child1",
            "children": [
                {"name": "grandchild1"},
                {"name": "grandchild2"}
            ]
        },
        {"name": "child2"}
    ]
}

VALID_NODE_EDGE_DATA = {
    "nodes": [
        {"name": "A"},
        {"name": "B"},
        {"name": "C"}
    ],
    "edges": [
        {"source": "A", "target": "B"},
        {"source": "B", "target": "C"}
    ]
}

COMPLEX_GRAPH_DATA = {
    "nodes": [
        {"name": "Node1"},
        {"name": "Node2"},
        {"name": "Node3"},
        {"name": "Node4"}
    ],
    "edges": [
        {"source": "Node1", "target": "Node2"},
        {"source": "Node2", "target": "Node3"},
        {"source": "Node3", "target": "Node4"},
        {"source": "Node1", "target": "Node4"}
    ]
}

# 测试工具函数
def assert_no_exception(func, *args, **kwargs):
    """
    断言函数不抛出异常
    
    Args:
        func: 要测试的函数
        *args: 函数的位置参数
        **kwargs: 函数的关键字参数
    """
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        pytest.fail(f"{func.__name__}() 抛出了意外的异常: {e}")

def create_invalid_data_variants():
    """
    创建各种无效数据的变体，用于负面测试
    
    Returns:
        dict: 包含各种无效数据的字典
    """
    return {
        "empty_data": {"data": []},
        "missing_data": {"width": 600, "height": 400},
        "invalid_theme": {"data": [{"time": "2018", "value": 99.9}], "theme": "invalid_theme"},
        "incomplete_data_items": {
            "data": [
                {"time": "2018"},  # 缺少 value
                {"value": 120.5}   # 缺少 time
            ]
        }
    }

def create_tree_data_variants():
    """
    创建各种树形数据的变体
    
    Returns:
        dict: 包含各种树形数据的字典
    """
    return {
        "missing_root_name": {"children": [{"name": "child1"}]},
        "missing_child_name": {
            "name": "root",
            "children": [{"name": "child1"}, {}]
        },
        "duplicate_children": {
            "name": "root",
            "children": [{"name": "duplicate"}, {"name": "duplicate"}]
        },
        "duplicate_across_levels": {
            "name": "root",
            "children": [{
                "name": "child1",
                "children": [{"name": "root"}]
            }]
        }
    }

def create_node_edge_data_variants():
    """
    创建各种节点边数据的变体
    
    Returns:
        dict: 包含各种节点边数据的字典
    """
    return {
        "missing_node_name": {
            "nodes": [{"name": "A"}, {}],
            "edges": []
        },
        "duplicate_nodes": {
            "nodes": [{"name": "A"}, {"name": "A"}],
            "edges": []
        },
        "missing_edge_source": {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [{"target": "B"}]
        },
        "missing_edge_target": {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [{"source": "A"}]
        },
        "invalid_edge_source": {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [{"source": "C", "target": "A"}]
        },
        "invalid_edge_target": {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [{"source": "A", "target": "C"}]
        },
        "duplicate_edges": {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "A", "target": "B"}
            ]
        }
    }

# Pytest fixtures
@pytest.fixture
def valid_area_data():
    """有效的面积图数据 fixture"""
    return VALID_AREA_CHART_DATA.copy()

@pytest.fixture
def valid_tree_data():
    """有效的树形数据 fixture"""
    return VALID_TREE_DATA.copy()

@pytest.fixture
def valid_graph_data():
    """有效的图形数据 fixture"""
    return VALID_NODE_EDGE_DATA.copy()
