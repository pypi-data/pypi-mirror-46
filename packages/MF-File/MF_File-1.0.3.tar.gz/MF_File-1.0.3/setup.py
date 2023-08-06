# coding=UTF-8
# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="MF_File",
    version="1.0.3",
    description="蝰蛇软件工作室-文件操作包",
    author="林睿霖",
    author_email="limitlin@outlook.com",
    url="https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_file_python",
    packages=find_packages(),
    install_requires=[
        "MF_StatusCode>=1.0.2"],
)
