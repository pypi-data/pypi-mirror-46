#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time   : 2019/3/1 16:46
# @Author : yebing
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : guozhi
# @FileName: PropHandler.py

from juice.model.ReplyMessage import ReplyMessage


class TaskHandler(object):
    """
        任务获取接口，只需实现handle方法，并调用reply方法即可
    """

    def __init__(self):
        self.id = None
        self.client = None
        self.type = None
        self.topic = None
        self.reply_message = None

    def execute(self, client, topic, message):
        self.id = message.id
        self.client = client
        self.type = message.type
        self.topic = topic
        self.handle(message)
        self._reply()

    def _reply(self):
        if self.reply_message is None:
            raise ValueError('reply message is not None')
        else:
            self.reply_message.id = self.id
            self.client.task_reply(self.reply_message)

    def reply(self, code=200, message='success', data=''):
        """
        上行消息,不允许重写
        :param code:
        :param message:
        :param data:
        :return:
        """
        self.reply_message = ReplyMessage(self.type + '_reply', code, message, data)

    def handle(self, message):
        """
        云端下发(下行)设置属性消息,需要重写接收flag进行处理
        :param message: JuiceMessage,原始的发送信息属性名称
            'id','type','data','time'
        """
        pass
