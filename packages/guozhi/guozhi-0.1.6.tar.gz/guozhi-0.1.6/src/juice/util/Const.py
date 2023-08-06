#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time   : 2019/5/23 14:31
# @Author : yebing
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : guozhi
# @FileName: Const.py

SUCCESS_CODE = 200
SUCCESS_MESSAGE = 'success'
SERVER_ERROR_CODE = 500

class Const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setter__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, 'Not allowed change const.{value}'.format(value=name)
        if not name.isupper():
            raise self.ConstCaseError, 'Consts name is not all uppercase'
        self.__dict__[name] = value




