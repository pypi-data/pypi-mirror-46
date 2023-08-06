# coding=utf-8
from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.0.5'
description = '简易图片采集工具,直接命令行运行就可以了，很简单～'
update = '提供命令行接口'
description = '{}。版本[{}]更新内容：{}'.format(description, version, update)

setup(
    name='image_collector',
    version=version,
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    url='https://github.com/Deali-Axy',
    # license='GPLv3',
    author='DealiAxy',
    author_email='dealiaxy@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'image_collector=image_collector.image_collector:run'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
