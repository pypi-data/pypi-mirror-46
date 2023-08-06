# coding:utf-8

import logging
from .code import ErrCode

ERROR = ErrCode


class ErrException(Exception):

    def __init__(self, e_err, extra=None, e=None):
        """
        :param e_err: 已定义的错误码枚举量，参见class Error定义，在HTTP错误码基础上扩展而来，左边加'E'，右边增加两位数字进行扩展，如E40001
        :param extra: 额外描述信息
        :param e: 其他异常对象
        """
        self.err = e_err
        self.extra = extra

        if self.extra is None:
            msg = 'throw ErrException[%s]-%s' % (self.err.code(), self.err.message())
        else:
            msg = 'throw ErrException[%s]-%s-%s' % (self.err.code(), self.err.message(), self.extra)

        logging.warning(msg, exc_info=True)

        if e is not None:
            logging.exception(e)
