# -*- coding: utf-8 -*-
# @author: yezxxx
# @contact: yezx@ebondmed.com
# @license: (C) CopyRight 2018-2018, EBondMed Tech. Co., Ltd limited
# @created at:  
# @project: ebondmedcore
# @file: apps.py
from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'transfer_api'
    def ready(self):
        import transfer_api.signals