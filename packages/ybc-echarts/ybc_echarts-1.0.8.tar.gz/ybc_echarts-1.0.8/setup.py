#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_echarts',
      version='1.0.8',
      description='ybc_echarts generate chart',
      long_description='ybc_echarts generate chart',
      author='lijz01',
      author_email='lijz01@fenbi.com',
      keywords=['pip3', 'ybc_echarts', 'python3','python','echats'],
      url='http://pip.zhenguanyu.com/',
      packages = ['ybc_echarts'],
      package_data={'ybc_echarts': ['__init__.py', 'ybc_echarts.py', 'ybc_echarts_unitest.py']},
      license='MIT',
      install_requires=['pyecharts', 'echarts-countries-pypkg', 'echarts-china-provinces-pypkg', 'echarts-china-cities-pypkg', 'ybc_exception', 'pyecharts-snapshot']
      )
