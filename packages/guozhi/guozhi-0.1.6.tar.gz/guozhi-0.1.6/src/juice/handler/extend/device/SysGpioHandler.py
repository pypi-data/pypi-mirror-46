#!/usr/bin/env python
# -*- coding:utf-8 -*-

from juice.handler.SysHandler import SysHandler
from juice.util import Const
from juice.util import GpioUtil


class GpioInitHandler(SysHandler):
    """
        GPIO针脚初始化
        handle为必须实现的方法
    """

    def handle(self, message):
        if isinstance(message.data, dict):
            status_code = Const.SUCCESS_CODE
            status_message = Const.SUCCESS_MESSAGE
            try:
                GpioUtil.initGPIOAccessType(
                    message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1),
                    message.data.get(GpioUtil.GPIO_CONST_ACCESS_TYPE, ''),
                    message.data.get(GpioUtil.GPIO_CONST_SIGNAL, ''))
            except Exception, err:
                status_code = Const.SERVER_ERROR_CODE
                status_message = 'failure: %s' % err
            self.reply(status_code, status_message)
        else:
            self.reply(Const.SERVER_ERROR_CODE, 'data is not dict')


class GpioSetHandler(SysHandler):
    """
        GPIO针脚电平设置(只支持GPIO.OUT模式)
        handle为必须实现的方法
    """

    def handle(self, message):
        if isinstance(message.data, dict):
            status_code = Const.SUCCESS_CODE
            status_message = Const.SUCCESS_MESSAGE
            try:
                GpioUtil.setGPIOStatus(
                    message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1),
                    message.data.get(GpioUtil.GPIO_CONST_SIGNAL, ''))
            except Exception, err:
                status_code = Const.SERVER_ERROR_CODE
                status_message = 'failure: %s' % err
            self.reply(status_code, status_message)
        else:
            self.reply(Const.SERVER_ERROR_CODE, 'data is not dict')


class GpioStatusGetHandler(SysHandler):
    """
    GPIO状态获取
    """

    def handle(self, message):
        if isinstance(message.data, dict):
            status_code = Const.SUCCESS_CODE
            status_message = Const.SUCCESS_MESSAGE
            data = GpioUtil.GetGPIOStatus(
                message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1))
            self.reply(status_code, status_message, data)
        else:
            self.reply(Const.SERVER_ERROR_CODE, 'data is not dict')
