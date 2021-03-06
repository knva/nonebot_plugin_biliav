#!/root/miniconda3/bin/python3 
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='nonebot_plugin_biliav',
    version="1.0.1",
    description=(
        'av号bv号查询器'
    ),
    long_description=open('README.md',encoding = 'utf_8').read(),
    long_description_content_type="text/markdown",
    author='knva',
    author_email='595902716@qq.com',
    maintainer='knva',
    maintainer_email='595902716@qq.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/knva/nonebot_plugin_biliav',
    install_requires=[
        'httpx',
    ]
)
