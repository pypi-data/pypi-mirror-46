"""
    processset - easy to scale computing processes
"""

from setuptools import setup, find_packages

setup(
    name="processset",
    version="0.0.3",
    author="zhengrenzhe",
    author_email="zhengrenzhe.niujie@gmail.com",
    description="easy to scale computing processes",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhengrenzhe/processset",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ]
)
