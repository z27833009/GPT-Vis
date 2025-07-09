"""
集成测试：测试所有验证函数的综合场景

该文件包含跨函数的集成测试，验证整个验证系统的协同工作

运行测试：
pytest __tests__/test_integration.py -v
"""

import pytest
from . import ValidationError, validate_params, validate_tree_data, validate_node_edge_data
from .conftest import assert_no_exception


class TestValidationIntegration:
    """验证函数的集成测试"""
    
    def test_all_validation_functions_available(self):
        """测试所有验证函数都可用"""
        # 确保所有函数都可以导入和调用
        assert callable(validate_params)
        assert callable(validate_tree_data)
        assert callable(validate_node_edge_data)
    
    def test_validation_error_consistency(self):
        """测试所有函数都使用一致的 ValidationError"""
        # 测试 validate_params
        with pytest.raises(ValidationError):
            validate_params("area", {})
        
        # 测试 validate_tree_data
        with pytest.raises(ValidationError):
            validate_tree_data({})
        
        # 测试 validate_node_edge_data
        with pytest.raises(ValidationError):
            validate_node_edge_data({
                "nodes": [{}],
                "edges": []
            })
    
    def test_real_world_chart_workflow(self):
        """测试真实世界的图表工作流"""
        # 模拟一个完整的图表生成流程
        chart_configs = [
            {
                "type": "area",
                "data": {
                    "data": [
                        {"time": "2018", "value": 99.9},
                        {"time": "2019", "value": 120.5},
                        {"time": "2020", "value": 88.2}
                    ],
                    "title": "销售趋势",
                    "theme": "default"
                }
            },
            {
                "type": "bar", 
                "data": {
                    "data": [
                        {"category": "产品A", "value": 100},
                        {"category": "产品B", "value": 200}
                    ]
                }
            }
        ]
        
        for config in chart_configs:
            try:
                validate_params(config["type"], config["data"])
            except (ValidationError, FileNotFoundError) as e:
                # 某些图表类型可能没有对应的 schema 文件
                if isinstance(e, FileNotFoundError):
                    pytest.skip(f"Schema for {config['type']} not found")
                else:
                    raise
    
    def test_complex_tree_and_graph_combination(self):
        """测试复杂的树形和图形数据组合"""
        # 组织架构树形数据
        org_tree = {
            "name": "公司",
            "children": [
                {
                    "name": "技术部",
                    "children": [
                        {"name": "前端组"},
                        {"name": "后端组"}
                    ]
                },
                {"name": "市场部"}
            ]
        }
        
        # 对应的协作关系图
        collaboration_graph = {
            "nodes": [
                {"name": "公司"},
                {"name": "技术部"},
                {"name": "市场部"},
                {"name": "前端组"},
                {"name": "后端组"}
            ],
            "edges": [
                {"source": "技术部", "target": "市场部"},
                {"source": "前端组", "target": "后端组"},
                {"source": "前端组", "target": "市场部"}
            ]
        }
        
        # 验证两种数据结构都有效
        assert validate_tree_data(org_tree) is True
        assert validate_node_edge_data(collaboration_graph) is True
    
    def test_data_transformation_pipeline(self):
        """测试数据转换管道"""
        # 模拟数据从一种格式转换到另一种格式的验证
        
        # 原始数据（图形格式）
        original_graph = {
            "nodes": [
                {"name": "A", "type": "root"},
                {"name": "B", "type": "child"},
                {"name": "C", "type": "child"}
            ],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "A", "target": "C"}
            ]
        }
        
        # 转换为树形格式
        transformed_tree = {
            "name": "A",
            "children": [
                {"name": "B"},
                {"name": "C"}
            ]
        }
        
        # 验证原始和转换后的数据都有效
        assert validate_node_edge_data(original_graph) is True
        assert validate_tree_data(transformed_tree) is True
    
    def test_error_message_quality(self):
        """测试错误消息的质量和一致性"""
        error_cases = [
            # validate_params 错误
            (lambda: validate_params("area", {}), "data"),
            
            # validate_tree_data 错误
            (lambda: validate_tree_data({}), "missing"),
            
            # validate_node_edge_data 错误  
            (lambda: validate_node_edge_data({
                "nodes": [{}], "edges": []
            }), "missing")
        ]
        
        for error_func, expected_keyword in error_cases:
            with pytest.raises(ValidationError) as exc_info:
                error_func()
            
            error_message = str(exc_info.value).lower()
            assert expected_keyword in error_message, f"Expected '{expected_keyword}' in error message: {error_message}"


class TestPerformanceIntegration:
    """性能相关的集成测试"""
    
    def test_large_dataset_performance(self):
        """测试大数据集的性能"""
        import time
        
        # 大型图表数据
        large_chart_data = {
            "data": [
                {"time": f"201{i}", "value": i * 10.5}
                for i in range(1000)
            ]
        }
        
        start_time = time.time()
        try:
            validate_params("area", large_chart_data)
        except (ValidationError, FileNotFoundError):
            pass  # 我们主要关注性能，不关心验证结果
        end_time = time.time()
        
        # 验证应该在合理时间内完成（1秒）
        assert end_time - start_time < 1.0, "Chart validation took too long"
        
        # 大型树形数据
        def create_deep_tree(depth):
            if depth <= 0:
                return {"name": f"leaf_{depth}"}
            return {
                "name": f"node_{depth}",
                "children": [create_deep_tree(depth - 1)]
            }
        
        deep_tree = create_deep_tree(100)
        
        start_time = time.time()
        validate_tree_data(deep_tree)
        end_time = time.time()
        
        assert end_time - start_time < 1.0, "Tree validation took too long"
        
        # 大型图形数据
        large_graph = {
            "nodes": [{"name": f"node_{i}"} for i in range(1000)],
            "edges": [
                {"source": f"node_{i}", "target": f"node_{(i+1) % 1000}"}
                for i in range(1000)
            ]
        }
        
        start_time = time.time()
        validate_node_edge_data(large_graph)
        end_time = time.time()
        
        assert end_time - start_time < 1.0, "Graph validation took too long"


class TestRobustnessIntegration:
    """健壮性相关的集成测试"""
    
    def test_unicode_handling_across_functions(self):
        """测试所有函数对 Unicode 字符的处理"""
        unicode_chart_data = {
            "data": [
                {"time": "2018年", "value": 99.9},
                {"time": "2019年", "value": 120.5}
            ],
            "title": "销售图表 📊"
        }
        
        unicode_tree = {
            "name": "根节点 🌳",
            "children": [
                {"name": "子节点 🍃"},
                {"name": "另一个子节点 🌿"}
            ]
        }
        
        unicode_graph = {
            "nodes": [
                {"name": "节点A 🅰️"},
                {"name": "节点B 🅱️"}
            ],
            "edges": [
                {"source": "节点A 🅰️", "target": "节点B 🅱️"}
            ]
        }
        
        # 所有函数都应该正确处理 Unicode
        try:
            validate_params("area", unicode_chart_data)
        except (ValidationError, FileNotFoundError):
            pass  # 可能因为其他原因失败，但不应该因为 Unicode 失败
        
        assert validate_tree_data(unicode_tree) is True
        assert validate_node_edge_data(unicode_graph) is True
    
    def test_memory_usage_with_large_data(self):
        """测试大数据集的内存使用"""
        import sys
        
        # 创建大数据集但不应该导致内存溢出
        large_datasets = [
            # 大图表数据
            {
                "data": [
                    {"time": f"day_{i}", "value": i}
                    for i in range(10000)
                ]
            },
            
            # 宽树形数据
            {
                "name": "root",
                "children": [
                    {"name": f"child_{i}"}
                    for i in range(1000)
                ]
            },
            
            # 大图形数据
            {
                "nodes": [{"name": f"node_{i}"} for i in range(5000)],
                "edges": [
                    {"source": f"node_{i}", "target": f"node_{(i+1) % 5000}"}
                    for i in range(5000)
                ]
            }
        ]
        
        for dataset in large_datasets:
            # 记录内存使用前的状态
            initial_objects = len(gc.get_objects()) if gc is not None else 0
            
            try:
                if "data" in dataset:
                    validate_params("area", dataset)
                elif "children" in dataset:
                    validate_tree_data(dataset)
                else:
                    validate_node_edge_data(dataset)
            except (ValidationError, FileNotFoundError):
                pass
            
            # 验证没有明显的内存泄漏
            # 这是一个简单的检查，实际内存管理更复杂
            if gc is not None:
                gc.collect()
                final_objects = len(gc.get_objects())
                # 对象数量增长应该在合理范围内
                assert final_objects - initial_objects < 10000, "Possible memory leak detected"
    
    def test_concurrent_validation(self):
        """测试并发验证的安全性"""
        import threading
        import time
        
        results = []
        errors = []
        
        def validate_worker(worker_id):
            try:
                # 每个线程执行不同的验证
                if worker_id % 3 == 0:
                    validate_params("area", {
                        "data": [{"time": f"2018_{worker_id}", "value": worker_id}]
                    })
                elif worker_id % 3 == 1:
                    validate_tree_data({
                        "name": f"root_{worker_id}",
                        "children": [{"name": f"child_{worker_id}"}]
                    })
                else:
                    validate_node_edge_data({
                        "nodes": [{"name": f"node_{worker_id}"}],
                        "edges": []
                    })
                results.append(f"Worker {worker_id} completed")
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # 创建多个并发线程
        threads = []
        for i in range(10):
            thread = threading.Thread(target=validate_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join(timeout=5.0)
        
        # 验证没有严重错误（某些 ValidationError 是预期的）
        serious_errors = [
            error for error in errors 
            if "ValidationError" not in error and "FileNotFoundError" not in error
        ]
        assert len(serious_errors) == 0, f"Serious errors in concurrent validation: {serious_errors}"


# 导入 gc 模块用于内存测试
try:
    import gc
except ImportError:
    gc = None
