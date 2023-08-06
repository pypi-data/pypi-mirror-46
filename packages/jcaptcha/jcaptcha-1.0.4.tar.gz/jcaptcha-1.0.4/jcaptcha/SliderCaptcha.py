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
from PIL import Image
from urllib.request import urlopen
import io


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "{base_dir}/data".format(base_dir=BASE_DIR)

# 容错偏差
CAPTCHA_X_OFFSET = 3


class SliderCaptcha(object):

    def __init__(self):
        pass

    def __call__(self, get_y=None, *args, **kwargs):
        # return self.get_captcha_image()
        if not get_y:
            get_y = 50
        if isinstance(get_y, (str, )):
            get_y = int(get_y)
        return self.get_slider_captcha_image(get_y)

    def get_slider_captcha_image(self, get_y):
        _slider_file_path = "{base_dir}/data/slider_63_60.png".format(base_dir=BASE_DIR)
        slider_file_path = "{base_dir}/temp_slider_captcha/{name}.png".format(base_dir=BASE_DIR, name=datetime.now().strftime('%Y%m%d%H%M%S'))

        fd = urlopen("http://images.sdgxgz.com/Pic{}.jpg".format(random.randint(1, 136)))
        image_file = io.BytesIO(fd.read())
        background = Image.open(image_file)
        foreground = Image.open(_slider_file_path)

        _x, _y = random.randint(50, 215), get_y
        background.paste(foreground, (_x, _y), foreground)
        # background.show()
        background.save(slider_file_path)
        # return slider_file_path
        image_data = open(slider_file_path, "rb").read()
        os.remove(slider_file_path)
        result = {
            "x":_x,
            "y":_y
        }
        # print("result=", result)
        return result, slider_file_path, image_data


slider_captcha = SliderCaptcha()