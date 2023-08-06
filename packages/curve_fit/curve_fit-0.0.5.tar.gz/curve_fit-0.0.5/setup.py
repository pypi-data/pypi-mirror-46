# -*- coding: utf-8 -*-
# @Project : curve_fit
# @Time    : 2019-05-27 14:21
# @Author  : Samuel Chan
# @Email   : samuelchan1205@gmail.com
# @File    : setup.py


import setuptools


# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="curve_fit",
    version="0.0.5",
    author="SamuelChan",
    author_email="samuelchan1205@gmail.com",
    description="Curve fit",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/samuel1205/curve_fit.git",
    packages=["curve_fit"],
    install_requires=[
        "numpy>=1.16.2",
        "patsy>=0.5.1",
        "statsmodels>=0.9.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
