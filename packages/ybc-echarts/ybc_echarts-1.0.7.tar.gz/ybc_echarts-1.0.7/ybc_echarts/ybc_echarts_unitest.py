# coding=utf-8
import unittest
from ybc_echarts import *


class MyTestCase(unittest.TestCase):
    def test_geo_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用__init__方法时，'title'、'subtitle'、'width'、'height'、'title_pos'、'title_top'参数类型错误。$"):
            Geo(123, 123, "", "", 123, 123)

    def test_geo_add_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用add方法时，'geo_cities_coords'参数类型错误。$"):
            geo = Geo()
            geo.add(1, 1, 1)


if __name__ == '__main__':
    unittest.main()