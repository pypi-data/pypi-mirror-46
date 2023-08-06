# coding=utf-8
from pyecharts import Geo as GetGeo

from ybc_exception import *


class Geo(GetGeo):

    @exception_handler('ybc_echarts')
    @params_check([
        ParamCheckEntry('Geo', object, is_not_empty),
        ParamCheckEntry('title', str, None),
        ParamCheckEntry('subtitle', str, None),
        ParamCheckEntry('width', int, None),
        ParamCheckEntry('height', int, None),
        ParamCheckEntry('title_pos', str, is_not_empty),
        ParamCheckEntry('title_top', str, is_not_empty)
    ])
    def __init__(
            self,
            title="",
            subtitle="",
            width=800,
            height=400,
            title_pos="auto",
            title_top="auto"
    ):

        super().__init__(title=title, subtitle=subtitle, width=width, height=height, title_pos=title_pos,
                         title_top=title_top)

    @exception_handler('ybc_echarts')
    @params_check([
        ParamCheckEntry('Geo', object, is_not_empty),
        ParamCheckEntry('attr', object, is_not_empty),
        ParamCheckEntry('value', object, is_not_empty),
        ParamCheckEntry('geo_cities_coords', dict, None)
    ])
    def add(
            self,
            attr="",
            value="",
            geo_cities_coords=None
    ):
        # 为了兼容现有教学代码 geo.add(counts.keys(),counts.values(),geo_cities_coords = all_coordinates)，不开放 name 参数
        self.__add('', attr, value, geo_cities_coords)


def __main__():
    geo = Geo('地图主标题', '地图副标题', title_pos='center', width=1600, height=800)
    geo.add(['北京', '长春'], [7, 2], geo_cities_coords={'北京朝阳': [116.44, 39.92], '吉林长春': [125.32, 43.9]})
    file_name = 'my.html'
    geo.render(file_name)


if __name__ == '__main__':
    __main__()