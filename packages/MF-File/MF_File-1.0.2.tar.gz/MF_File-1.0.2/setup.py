# coding=UTF-8
# from distutils.core import setup
from setuptools import setup, find_packages
import MF_File

setup(
    name="MF_File",
    version=MF_File.__version__,
    description="蝰蛇软件工作室-文件操作包",
    author="林睿霖",
    author_email="limitlin@outlook.com",
    url="https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_file_python",
    packages=find_packages(),
    install_requires=[
        "MF_StatusCode>=1.0.1"],
)
