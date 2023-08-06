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

import json
import uuid


class JuiceMessage(object):
    def __init__(self, jtype, data, time):
        self.id = str(uuid.uuid1())
        self.type = jtype
        self.data = data
        self.time = time

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'type': self.type,
            'data': self.data,
            'time': self.time
        })

    __repr__ = __str__


if __name__ == '__main__':
    aa = JuiceMessage("asdasd", "flag", {"gpio_num": 0, "mode": "bcm"})
    print type(aa)
    print str(aa)
