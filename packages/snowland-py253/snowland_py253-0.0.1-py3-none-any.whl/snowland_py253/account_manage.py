#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: account_manage.py
# @time: 2019/5/13 16:03
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_py253.account import Account
import requests
from snowland_py253.common import (
    PY253_BALANCE_GET_URI, BASE_URI
)


class AccountManage(Account):
    def __init__(self, account=None, password=None, uri=BASE_URI):
        Account.__init__(self, account, password, uri)

    def get_user_balance(self):
        """
        取账户余额
        """
        params = self.public_params()
        return requests.post(self.uri + PY253_BALANCE_GET_URI, json=params).json()
