# -*- coding: utf-8 -*-
# @author: yezxxx
# @contact: yezx@ebondmed.com
# @license: (C) CopyRight 2018-2018, EBondMed Tech. Co., Ltd limited
# @created at:  
# @project: ebondmedcore
# @file: forms.py

import django_filters

from .models import TransHospitalTransact, InHospitalTransact


class NullFilter(django_filters.BooleanFilter):
    """
    NullFilter Class serves for backlog unattributed objects
    ------------------------------
    """

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.field_name: value})
        return qs


class TransHospitalTransactFilter(django_filters.FilterSet):
    """docstring"""

    class Meta:
        model = TransHospitalTransact
        fields = ('from_hospital', 'to_hospital',
                  'from_practitioner', 'to_practitioner', 'PatientRecord',
                  'order_sn', 'trade_sn',
                  'open_time',
                  'transact_status', 'pay_time')


class InHospitalTransactFilter(django_filters.FilterSet):
    """docstring"""

    class Meta:
        model = InHospitalTransact
        fields = (
            'order_sn', 'trade_sn', 'open_time', 'transact_status', 'transact_comments', 'pay_time',
            'next_order')
