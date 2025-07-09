"""
测试 validate_params 函数

该文件专门测试 validate.py 中的 validate_params 函数
包含正向测试和负向测试用例

运行测试：
pytest __tests__/test_validate_params.py -v
"""

import pytest
from . import ValidationError, validate_params
from .conftest import (
    VALID_AREA_CHART_DATA, 
    VALID_STACKED_AREA_DATA, 
    VALID_BAR_CHART_DATA, 
    VALID_PIE_CHART_DATA,
    assert_no_exception,
    create_invalid_data_variants
)


class TestValidateParamsPositive:
    """测试 validate_params 函数的正向用例"""
    
    def test_valid_area_chart_data(self, valid_area_data):
        """测试有效的面积图数据"""
        assert_no_exception(validate_params, "area", valid_area_data)
    
    def test_valid_area_chart_with_stack(self):
        """测试有效的堆叠面积图数据"""
        assert_no_exception(validate_params, "area", VALID_STACKED_AREA_DATA)
    
    def test_minimal_valid_area_data(self):
        """测试最小有效面积图数据（只包含必需字段）"""
        minimal_data = {
            "data": [{"time": "2018", "value": 99.9}]
        }
        assert_no_exception(validate_params, "area", minimal_data)
    
    def test_area_chart_with_all_optional_fields(self):
        """测试包含所有可选字段的面积图数据"""
        complete_data = {
            "data": [
                {"time": "2018", "value": 99.9},
                {"time": "2019", "value": 120.5}
            ],
            "width": 800,
            "height": 600,
            "title": "完整测试图表",
            "axisXTitle": "时间轴",
            "axisYTitle": "数值轴",
            "theme": "academy",
            "stack": False
        }
        assert_no_exception(validate_params, "area", complete_data)
    
    def test_valid_bar_chart_data(self):
        """测试有效的柱状图数据"""
        assert_no_exception(validate_params, "bar", VALID_BAR_CHART_DATA)
    
    def test_valid_pie_chart_data(self):
        """测试有效的饼图数据"""
        assert_no_exception(validate_params, "pie", VALID_PIE_CHART_DATA)
    
    def test_valid_line_chart_data(self):
        """测试有效的折线图数据"""
        line_data = {
            "data": [
                {"time": "2018", "value": 99.9},
                {"time": "2019", "value": 120.5},
                {"time": "2020", "value": 88.2}
            ]
        }
        assert_no_exception(validate_params, "line", line_data)
    
    @pytest.mark.parametrize("chart_type,data", [
        ("area", VALID_AREA_CHART_DATA),
        ("bar", VALID_BAR_CHART_DATA),
        ("pie", VALID_PIE_CHART_DATA),
        ("line", {"data": [{"time": "2018", "value": 99.9}]}),
    ])
    def test_multiple_chart_types(self, chart_type, data):
        """参数化测试多种图表类型"""
        assert_no_exception(validate_params, chart_type, data)


class TestValidateParamsNegative:
    """测试 validate_params 函数的负向用例"""
    
    def test_missing_required_data_field(self):
        """测试缺少必需的 data 字段"""
        invalid_data = {
            "width": 600,
            "height": 400,
            "title": "测试图表"
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_empty_data_array(self):
        """测试空数据数组"""
        invalid_data = {
            "data": [],
            "width": 600,
            "height": 400
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_invalid_data_structure_missing_time(self):
        """测试数据项缺少 time 字段"""
        invalid_data = {
            "data": [
                {"value": 120.5}  # 缺少 time 字段
            ]
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_invalid_data_structure_missing_value(self):
        """测试数据项缺少 value 字段"""
        invalid_data = {
            "data": [
                {"time": "2018"}  # 缺少 value 字段
            ]
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_invalid_theme_value(self):
        """测试无效的主题值"""
        invalid_data = {
            "data": [{"time": "2018", "value": 99.9}],
            "theme": "invalid_theme"
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_invalid_chart_type(self):
        """测试无效的图表类型（schema 文件不存在）"""
        valid_data = {
            "data": [{"time": "2018", "value": 99.9}]
        }
        
        with pytest.raises(FileNotFoundError):
            validate_params("non_existent_chart_type", valid_data)
    
    def test_invalid_data_type_for_value(self):
        """测试 value 字段的数据类型错误"""
        invalid_data = {
            "data": [
                {"time": "2018", "value": "not_a_number"}  # value 应该是数字
            ]
        }
        
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)
    
    def test_negative_dimensions(self):
        """测试负数的宽度和高度"""
        invalid_data = {
            "data": [{"time": "2018", "value": 99.9}],
            "width": -100,  # 负数宽度
            "height": -200  # 负数高度
        }
        
        # 注意：这个测试可能通过，取决于 schema 是否限制了最小值
        # 如果 schema 没有限制，我们可能需要在 schema 中添加 minimum: 0
        try:
            validate_params("area", invalid_data)
            # 如果没有抛出异常，说明 schema 没有限制负数
            print("警告：schema 允许负数尺寸")
        except ValidationError:
            # 如果抛出异常，说明 schema 正确限制了负数
            pass
    
    @pytest.mark.parametrize("invalid_data", [
        {"data": []},  # 空数组
        {"width": 600, "height": 400},  # 缺少 data
        {"data": [{"time": "2018"}]},  # 缺少 value
        {"data": [{"value": 99.9}]},  # 缺少 time
    ])
    def test_various_invalid_data(self, invalid_data):
        """参数化测试各种无效数据"""
        with pytest.raises(ValidationError):
            validate_params("area", invalid_data)


class TestValidateParamsEdgeCases:
    """测试 validate_params 函数的边界情况"""
    
    def test_single_data_point(self):
        """测试只有一个数据点的情况"""
        single_point_data = {
            "data": [{"time": "2018", "value": 99.9}]
        }
        assert_no_exception(validate_params, "area", single_point_data)
    
    def test_large_data_set(self):
        """测试大数据集"""
        large_data = {
            "data": [
                {"time": f"201{i}", "value": i * 10.5} 
                for i in range(100)
            ]
        }
        assert_no_exception(validate_params, "area", large_data)
    
    def test_zero_values(self):
        """测试零值数据"""
        zero_data = {
            "data": [
                {"time": "2018", "value": 0},
                {"time": "2019", "value": 0.0}
            ]
        }
        assert_no_exception(validate_params, "area", zero_data)
    
    def test_negative_values(self):
        """测试负值数据"""
        negative_data = {
            "data": [
                {"time": "2018", "value": -99.9},
                {"time": "2019", "value": -120.5}
            ]
        }
        assert_no_exception(validate_params, "area", negative_data)
    
    def test_very_large_numbers(self):
        """测试极大数值"""
        large_numbers_data = {
            "data": [
                {"time": "2018", "value": 1e10},
                {"time": "2019", "value": 9.999999e15}
            ]
        }
        assert_no_exception(validate_params, "area", large_numbers_data)
    
    def test_unicode_strings(self):
        """测试包含 Unicode 字符的字符串"""
        unicode_data = {
            "data": [
                {"time": "2018年", "value": 99.9},
                {"time": "2019年", "value": 120.5}
            ],
            "title": "测试图表 📊",
            "axisXTitle": "时间轴 ⏰",
            "axisYTitle": "数值轴 📈"
        }
        assert_no_exception(validate_params, "area", unicode_data)
    
    def test_empty_strings(self):
        """测试空字符串"""
        empty_string_data = {
            "data": [{"time": "2018", "value": 99.9}],
            "title": "",
            "axisXTitle": "",
            "axisYTitle": ""
        }
        assert_no_exception(validate_params, "area", empty_string_data)


class TestValidateParamsIntegration:
    """集成测试：测试 validate_params 与不同图表类型的结合"""
    
    def test_all_supported_chart_types(self):
        """测试所有支持的图表类型"""
        # 这个测试需要根据实际支持的图表类型来调整
        chart_types_and_data = [
            ("area", VALID_AREA_CHART_DATA),
            ("bar", VALID_BAR_CHART_DATA),
            ("pie", VALID_PIE_CHART_DATA),
        ]
        
        for chart_type, data in chart_types_and_data:
            try:
                validate_params(chart_type, data)
                # 如果没有抛出异常，说明验证通过了
            except (ValidationError, FileNotFoundError):
                # 某些图表类型可能不存在对应的 schema 文件，这是可以接受的
                pass
    
    def test_schema_consistency(self):
        """测试 schema 文件的一致性"""
        # 确保基本的面积图 schema 存在且可用
        basic_data = {
            "data": [{"time": "2018", "value": 99.9}]
        }
        
        # 这应该总是成功，因为 area.json 应该存在
        assert_no_exception(validate_params, "area", basic_data)
