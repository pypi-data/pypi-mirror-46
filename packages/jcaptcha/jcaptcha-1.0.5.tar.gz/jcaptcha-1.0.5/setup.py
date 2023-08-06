#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages, Extension


setup(
    name='jcaptcha',
      version='1.0.5',
      description='验证码生成',
      long_description = "简单图片验证、滑块验证",
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