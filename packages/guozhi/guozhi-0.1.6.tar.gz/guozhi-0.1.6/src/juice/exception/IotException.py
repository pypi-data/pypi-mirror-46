#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


class IotException(Exception):
    """
        iot异常
    """

    def __init__(self, message, code=200):
        self.code = code
        self.message = message

    def __str__(self):
        return json.dumps({
            'code': self.code,
            'message': self.message
        })
