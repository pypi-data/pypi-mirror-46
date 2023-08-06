import unittest
from ybc_coordinate import *


class MyTestCase(unittest.TestCase):
    def test_list_provinces(self):
        self.assertIsNotNone(list_provinces())

    def test_get_province(self):
        self.assertEqual(get_coordinate('北京', '朝阳'), [116.44, 39.92])

    def test_get_province_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用get_coordinate方法时，'province'、'city'参数类型错误。$"):
            get_coordinate(123, 123)

    def test_get_province_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用get_coordinate方法时，'province'参数不在允许范围内。$"):
            get_coordinate('', '')


if __name__ == '__main__':
    unittest.main()
