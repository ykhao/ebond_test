# -*- coding: utf-8 -*-
# @author: yezxxx
# @contact: yezx@ebondmed.com
# @license: (C) CopyRight 2018-2018, EBondMed Tech. Co., Ltd limited
# @created at:  
# @project: ebondmedcore
# @file: urls.py
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'auth', views.UserViewSet)
