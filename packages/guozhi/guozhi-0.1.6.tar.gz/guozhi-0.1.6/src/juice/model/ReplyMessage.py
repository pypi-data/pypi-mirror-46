#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time   : 2019/3/1 16:00
# @Author : yebing
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : guozhi
# @FileName: ReplyMessage.py

import json
import time
import uuid


class ReplyMessage(object):
    def __init__(self, type_name, code, message, data):
        self.id = str(uuid.uuid1())
        self.type = type_name
        self.data = {
            'code': code,
            'message': message,
            'data': data
        }
        self.time = int(round(time.time() * 1000))

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'type': self.type,
            'time': self.time,
            'data': self.data
        })

    __repr__ = __str__


if __name__ == '__main__':
    aa = ReplyMessage("flag", 200, 'asd', {"gpio_num": 0, "mode": "bcm"})
    print aa
