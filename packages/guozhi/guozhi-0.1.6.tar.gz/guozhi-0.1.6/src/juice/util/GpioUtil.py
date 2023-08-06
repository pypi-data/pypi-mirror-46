#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import warnings

import RPi.GPIO as GPIO

from juice.exception.IotException import IotException

GPIO_STATUS = {-1: 'no mode,please input bcm or board', 0: 'LOW', 1: 'HIGH'}
GPIO_MODE = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}
GPIO_CONST_MODE = 'mode'
GPIO_CONST_NUM = 'gpio_num'
GPIO_CONST_SIGNAL = 'signal'
GPIO_CONST_ACCESS_TYPE = 'access_type'


def checkMode(mode):
    """
    判断模式是否支持
    :param mode:
    :return:
    """
    mode_type = GPIO_MODE.get(mode.lower(), '')
    if mode_type == '':
        raise IotException('mode is error,please input %s or %s' % ('bcm', 'board'), 404)
    else:
        return mode_type


def GetGPIOStatus(mode, gpio_num):
    """
    根据模式和针脚号获得该针脚的状态
    :param mode: 模式，只能是bcm或board
    :param gpio_num: 对应模式的针脚号
    :return: LOW 或 HIGH
    """
    checkMode(mode)

    return json.dumps({
        'mode': mode,
        'gpio_num': gpio_num,
        'access_type': GetGPIOType(mode, gpio_num),
        'signal': GetGPIOStatusNum(mode, gpio_num)
    })


def GetGPIOStatusNum(mode, gpio_num):
    """
    根据模式和针脚号获得该指针的高低电平
    :param mode:
    :param gpio_num:
    :return: -1(无效),0(低),1(高)
    """

    mode_type = checkMode(mode.lower())
    GPIO.setwarnings(True)
    GPIO.setmode(mode_type)
    with warnings.catch_warnings(record=True) as w:
        GPIO.setup(gpio_num, GPIO.gpio_function(gpio_num))
    return GPIO.input(gpio_num)


def GetGPIOType(mode, gpio_num):
    """
    根据模式和针脚号获得目前是输入还是输出
    :param mode:
    :param gpio_num:
    :return:
    """
    mode_type = checkMode(mode.lower())
    GPIO.setwarnings(True)
    GPIO.setmode(mode_type)
    return GPIO.gpio_function(gpio_num)


def initGPIOAccessType(mode, gpio_num, accesstype, signal):
    """
    初始化gpio的接入方式，强制初始化
    :param mode:
    :param gpio_num:
    :param accesstype: 接入类型对应GPIO.in(1),GPIO.out(0)
    :param signal: 高低电平对应GPIO.HIGH(1),GPIO.LOW(0)
    :return:
    """
    mode_type = checkMode(mode.lower())
    GPIO.setwarnings(False)
    GPIO.setmode(mode_type)
    if accesstype == 1:
        # signal取GPIO.PUD_DOWN,GPIO.PUD_UP,GPIO.PUD_OFF
        if signal in [GPIO.PUD_DOWN, GPIO.PUD_UP, GPIO.PUD_OFF]:
            GPIO.setup(gpio_num, accesstype, pull_up_down=signal)
        else:
            raise IotException('GPIO.IN not support signal(GPIO.PUD_OFF(20),GPIO.PUD_DOWN(21), GPIO.PUD_UP(22))',
                               500)
    else:
        # signal取GPIO.IN,GPIO.OUT
        if signal in [GPIO.IN, GPIO.OUT]:
            GPIO.setup(gpio_num, accesstype, initial=signal)
        else:
            raise IotException('GPIO.IN not support signal(GPIO.IN, GPIO.OUT)', 500)


def setGPIOStatus(mode, gpio_num, signal):
    """
    设置gpio针脚电平，当为gpio.input模式，不允许设置
    :param mode:
    :param gpio_num:
    :param signal:
    :return:
    """
    mode_type = checkMode(mode.lower())
    GPIO.setwarnings(True)
    GPIO.setmode(mode_type)
    if GPIO.IN == GPIO.gpio_function(gpio_num):
        raise IotException('access type error,please set GPIO stitch for GPIO.OUT', 400)
    with warnings.catch_warnings(record=True) as w:
        GPIO.setup(gpio_num, GPIO.gpio_function(gpio_num))
        GPIO.output(gpio_num, signal)
