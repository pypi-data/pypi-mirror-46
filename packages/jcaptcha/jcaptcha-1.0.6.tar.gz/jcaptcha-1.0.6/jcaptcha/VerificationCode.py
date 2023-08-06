#!/usr/bin/env python
# encoding: utf-8


from captcha.image import ImageCaptcha
import numpy as  np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import random
import os
from datetime import datetime

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "{base_dir}/data".format(base_dir=BASE_DIR)


class jCaptcha(object):
    language = "zh" # 默认显示中文

    def __init__(self):
        pass

    def __call__(self, language=None, *args, **kwargs):
        if language:
            self.language = language
        return self.get_captcha_image()

    def random_captcha_text(self, char_set=number + alphabet + Alphabet, captcha_size=4):
        """
            生成验证码位数：支持数字、大小写字母，默认长度4
        :param char_set:
        :param captcha_size:
        :return:
        """
        captcha_text = []
        for i in range(captcha_size):
            c = random.choice(char_set)
            captcha_text.append(c)
        return captcha_text

    def captcha_expression(self, captcha_type=1, captcha_size=1, is_random_lenth=True, is_combination=False):
        """
            生成表达式验证码：
        :param captcha_type: +-*/(1~4)，目前支持+
        :param captcha_size: 单个验证码长度
        :param is_random_lenth: 是否随机长度
        :param is_combination: 是否组合(+-*/)
        :return:
        """
        captcha_type_dict = {
            1: {"symbol": "+", "desc": "加", "zh_name": "加", "en_name": "+"},
            2: {"symbol": "-", "desc": "减", "zh_name": "减", "en_name": "-"},
            3: {"symbol": "*", "desc": "乘", "zh_name": "乘", "en_name": "*"},
            4: {"symbol": "/", "desc": "除", "zh_name": "除", "en_name": "/"},
        }

        if captcha_size in (2, ) and is_random_lenth: captcha_size += 3-captcha_size
        a = self.random_captcha_text(char_set=number, captcha_size=1 if captcha_size < 3 else random.choice(range(1, captcha_size)))
        b = self.random_captcha_text(char_set=number, captcha_size=1 if captcha_size < 3 else random.choice(range(1, captcha_size)))

        a = "".join(a)
        b = "".join(b)
        expression_symbol = "{a} {captcha_type} {b}".format(a=a,b=b,captcha_type=captcha_type_dict[captcha_type]["symbol"])
        expression_desc = "{a} {captcha_type} {b}".format(a=a,b=b,captcha_type=captcha_type_dict[captcha_type]["{}_name".format(self.language)])
        expression_result = eval(expression_symbol)
        # expression = expression + "=?"
        return expression_desc, expression_result


    def gen_captcha_text_and_image(self):
        """
            使用ImageCaptcha库生成验证码
        :return:
        """
        image = ImageCaptcha(width=160, height=60, fonts=["{FONTS_DIR}/SIMYOU.TTF".format(FONTS_DIR=DATA_DIR)])
        # captcha_text = self.random_captcha_text()
        captcha_text, expression_result = self.captcha_expression()
        # captcha_text = ''.join(captcha_text)
        captcha = image.generate(captcha_text)
        captcha_image = Image.open(captcha)
        captcha_image = np.array(captcha_image)
        return captcha_text, captcha_image, expression_result

    def get_captcha_image(self):
        """
        输出验证码
        :return:
        """
        text, image, result = self.gen_captcha_text_and_image()
        plt.imshow(image)
        plt.axis('off')  # 不显示坐标轴
        dir_name = "{base_dir}/v_code".format(base_dir=BASE_DIR)
        file_name = "{name}.png".format(name=datetime.now().strftime('%Y%m%d%H%M%S'))
        file_path = dir_name + '/' + file_name
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        plt.savefig(file_path)
        image_data = open(file_path, "rb").read()
        os.remove(file_path)
        return text, result, file_path, image_data

jcaptcha = jCaptcha()