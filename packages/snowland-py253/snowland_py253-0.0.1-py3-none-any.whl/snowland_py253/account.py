#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: account.py
# @time: 2019/5/13 10:35
# @Software: PyCharm


__author__ = 'A.Star'
from snowland_authsdk.login import Account as AuthAccount
from snowland_py253.common import BASE_URI


class Account(AuthAccount):
    def __init__(self, account=None, password=None, uri=BASE_URI, **kwargs):
        AuthAccount.__init__(self, access_key=account, access_secret=password)
        self.uri = uri


    def public_params(self):
        return {'account': self.access_key, 'password': self.access_secret}
