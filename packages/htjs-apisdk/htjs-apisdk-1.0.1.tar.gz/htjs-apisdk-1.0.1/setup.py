# -*- coding:utf-8 -*-

import setuptools
from htjs_apisdk import HTJS_API_SDK_VERSION

setuptools.setup(
    name="htjs-apisdk",
    version=HTJS_API_SDK_VERSION,
    keywords=("htjs", "htjs.net"),
    author="Mu Xiaofei",
    author_email="htjs.net@gmail.com",
    description="HtjsApiClient",
    long_description="",
    long_description_content_type="text/x-rst",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["six"],
)
