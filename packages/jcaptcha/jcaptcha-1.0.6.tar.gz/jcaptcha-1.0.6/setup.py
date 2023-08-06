#!/usr/bin/env python
# encoding: utf-8
import os
from setuptools import setup, find_packages, Extension


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='jcaptcha',
      version='1.0.6',
      description='验证码生成',
      # long_description = "简单图片验证、滑块验证",
      long_description = read('README.rst'),
      url='https://github.com/xiaofeng283/jcaptcha',
      author='Jervon',
      author_email='xiaofeng283@gmail.com',
      license='MIT',
      packages = ['jcaptcha'],
      include_package_data = True,
      package_dir={'jcaptcha': 'jcaptcha',},
      zip_safe=False,
      install_requires = [
        "captcha",
        "numpy",
        "matplotlib",
        "Pillow",
        ]
)