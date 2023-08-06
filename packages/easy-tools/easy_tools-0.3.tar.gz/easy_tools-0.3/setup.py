from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="easy_tools",
    version="0.3",
    author="Jayanth Sai",
    author_email="jayanthsai1998@gmail.com",
    description="easy_tools is a package that helps to perform easy operations on iterables with less time complexity",
    url="https://github.com/jayanthsai1998/EasyTools",
    license='MIT',
    packages=['easy_tools'],
    zip_safe=False
)
