# -*- coding:utf-8 -*-

import setuptools

setuptools.setup(
    name="kmux",
    version="0.0.11",
    keywords=("rest",),
    author="Xiaofei Mu",
    author_email="me@muxiaofei.cn",
    description="Easy for restful dev",
    long_description="",
    long_description_content_type="text/x-rst",
    url="https://gitee.com/muxiaofei/kmux",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson"],
)
