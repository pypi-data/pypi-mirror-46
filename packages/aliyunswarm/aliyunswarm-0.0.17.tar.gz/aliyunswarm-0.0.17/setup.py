import setuptools
import os
import sys

REQUIRED_PYTHON = (3, 6)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='aliyunswarm',
      python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
      version='0.0.17',
      author='rocky',
      author_email='lingyu.cheng@gmail.com',
      description='aliyun swarm api',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/rockercheng/AliyunSwarm',
      packages=setuptools.find_packages(),
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
