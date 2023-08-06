#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: internal_message.py
# @time: 2019/5/13 10:46
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_py253.account import Account
import requests
from snowland_py253.common import (
    PY253_SMS_SEND_URI, BASE_URI
)
import urllib


class InternalMessage(Account):
    """
    国内短信接口
    """
    def __init__(self, account=None, password=None, uri=BASE_URI):
        Account.__init__(self, account, password, uri)

    def send_sms(self, text, phone, report=False):
        """
        用接口发短信
        """
        assert isinstance(phone, str)
        send_sms_params = {
            'msg': urllib.request.quote(text),
            'phone': phone,
            'report': report
        }
        params = dict(self.public_params(), **send_sms_params)
        return requests.post(self.uri + PY253_SMS_SEND_URI, json=params).json()
