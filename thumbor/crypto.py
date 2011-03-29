#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import base64

from pyDes import *

from thumbor.url import Url

class Crypto(object):
    def __init__(self, salt):
        self.salt = (salt * 24)[:24]

    def encrypt(self, 
                width,
                height,
                smart,
                flip_horizontal,
                flip_vertical,
                halign,
                valign,
                crop_left,
                crop_top,
                crop_right,
                crop_bottom):

        url = Url.generate_options(width,
                                   height,
                                   smart,
                                   False,
                                   flip_horizontal,
                                   flip_vertical,
                                   halign,
                                   valign,
                                   crop_left,
                                   crop_top,
                                   crop_right,
                                   crop_bottom)

        key = triple_des(self.salt,
                         CBC, 
                         '\0\0\0\0\0\0\0\0', 
                         pad=None, 
                         padmode=PAD_PKCS5)

        return base64.urlsafe_b64encode(key.encrypt(url))

    def decrypt(self, encrypted):

        key = triple_des(self.salt,
                         CBC, 
                         '\0\0\0\0\0\0\0\0', 
                         pad=None, 
                         padmode=PAD_PKCS5)

        decrypted = key.decrypt(base64.urlsafe_b64decode(encrypted))

        if not decrypted:
            return None

        return Url.parse_options(decrypted)
