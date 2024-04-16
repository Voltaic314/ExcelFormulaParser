import pytest
from Objects.constant import Constant


class TestConstant:
    
    def test_is_valid_constant_with_numbers(self):
        assert Constant.is_valid_constant('123') == True
        assert Constant.is_valid_constant('45.67') == True

    def test_is_valid_constant_with_invalid_data(self):
        with pytest.raises(ValueError):
            Constant.is_valid_constant('abc')
        with pytest.raises(ValueError):
            Constant.is_valid_constant('123abc')

    def test_parse_constant_int(self):
        const = Constant(123)
        assert const.parse_constant('456') == 456

    def test_parse_constant_float(self):
        const = Constant(123.0)
        assert const.parse_constant('456.78') == 456.78

    def test_parse_constant_with_non_string_input(self):
        const = Constant(123)
        assert const.parse_constant(456) == 456

    def test_parse_constant_raises_error(self):
        const = Constant(123)
        with pytest.raises(ValueError):
            const.parse_constant('abc')
        with pytest.raises(ValueError):
            const.parse_constant('123abc')
        with pytest.raises(ValueError):
            const.parse_constant('!@#$%^')

    def test_str(self):
        const = Constant(123)
        assert str(const) == '123'

    def test_to_dict(self):
        const = Constant(456)
        assert const.to_dict() == {'constant': 456}

