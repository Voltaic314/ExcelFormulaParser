import pytest
from Models.constant import Constant

class TestConstant:
    
    def test_is_valid_constant_with_numbers(self):
        assert Constant.is_valid_constant('123') == True
        assert Constant.is_valid_constant('45.67') == False  # This should be False as '45.67'.isdigit() will return False

    def test_is_valid_constant_with_invalid_data(self):
        assert Constant.is_valid_constant('abc') == False
        assert Constant.is_valid_constant('123abc') == False

    def test_constant_initialization_valid(self):
        const_int = Constant('456')
        assert const_int.value == 456
        const_float = Constant('456.78')
        assert const_float.value == 456.78

    def test_constant_initialization_invalid(self):
        with pytest.raises(ValueError):
            Constant('abc')
        with pytest.raises(ValueError):
            Constant('123abc')
        with pytest.raises(ValueError):
            Constant('!@#$%^')

    def test_str(self):
        const = Constant('123')
        assert str(const) == '123'

    def test_to_dict(self):
        const = Constant('456')
        assert const.to_dict() == {'constant': 456}

    def test_from_dict(self):
        const = Constant.from_dict({'constant': 456})
        assert const.value == 456
        assert isinstance(const, Constant)