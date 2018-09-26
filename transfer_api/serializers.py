# -*- coding: utf-8 -*-
# @author: yezxxx
# @contact: yezx@ebondmed.com
# @license: (C) CopyRight 2018-2018, EBondMed Tech. Co., Ltd limited
# @created at:  
# @project: ebondmedcore
# @file: serializers.py

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import TransHospitalTransact, InHospitalTransact


class TransHospitalTransactSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = TransHospitalTransact
        fields = ('id', 'from_hospital', 'to_hospital',
                  'from_practitioner', 'to_practitioner', 'PatientRecord',
                  'order_sn', 'trade_sn',
                  'open_time',
                  'transact_status', 'pay_time', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('transhospitaltransact-detail',
                            kwargs={'pk': obj.pk}, request=request)
        }


class InHospitalTransactSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = InHospitalTransact
        fields = (
            'order_sn', 'trade_sn', 'open_time', 'transact_status',
            'transact_comments', 'pay_time',
            'next_order', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('inhospitaltransact-detail',
                            kwargs={'pk': obj.pk}, request=request)
        }
