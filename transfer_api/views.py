# -*- coding: utf-8 -*-
# @author: yezxxx
# @contact: yezx@ebondmed.com
# @license: (C) CopyRight 2018-2018, EBondMed Tech. Co., Ltd limited
# @created at:  
# @project: ebondmedcore
# @file: views.py

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, authentication, permissions, filters
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerAndReadOnly
from rest_framework.views import APIView
from .models import TransHospitalTransact
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .forms import TransHospitalTransactFilter, InHospitalTransactFilter
from .models import TransHospitalTransact, InHospitalTransact
from .serializers import TransHospitalTransactSerializer, \
    InHospitalTransactSerializer
from data_api.models import MedicalRecord


class DefaultMixin(object):
    """
    Default views settings, to be successed by other viewsets.
    """
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
        JSONWebTokenAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated, IsOwnerAndReadOnly)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class TransHospitalTransactViewSet(DefaultMixin, viewsets.ModelViewSet):
    """docstring"""

    queryset = TransHospitalTransact.objects.all()
    serializer_class = TransHospitalTransactSerializer
    filter_class = TransHospitalTransactFilter
    search_fields = ('from_hospital', 'to_hospital',
                  'from_practitioner', 'to_practitioner', 'PatientRecord',
                  'order_sn', 'trade_sn',
                  'open_time',
                  'transact_status', 'pay_time')
    ordering_fields = (
        'from_hospital', 'order_sn', 'trade_sn', 'open_time', 'pay_time')

    @action(detail=True, methods=['GET'])
    def get_transact_status(self, request, *args, **kwargs):
        """
        get transact_status(detail)
        :param request:
        :param args:
        :param kwargs:
        :return: transact.transact_status
        """
        transact = self.get_object()
        return Response(transact.transact_status)

    @action(detail=True, methods=['PATCH'])
    def patch_medical_record_from_transact_status(self, request, pk=None,
                                                  *args,
                                        **kwargs):
        transact = TransHospitalTransact.objects.get(pk=pk)
        serializer = TransHospitalTransactSerializer(transact,
                                                     data=request.data[
                                                         'transact_status'])
        if serializer.is_valid():
            serializer.update(transact, serializer)
            if request.data['transact_status'] == 'TRANS_ACCEPTED':
                try:
                    medical_record = MedicalRecord.objects.get(
                        prescribe_practitioner=transact.from_practitioner)
                    medical_record.prescribe_practitioner = transact.to_practitioner
                    return Response(serializer.data['transact_status'],
                                    status=status.HTTP_206_PARTIAL_CONTENT)
                except MedicalRecord.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data['transact_status'],
                            status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class InHospitalTransactViewSet(DefaultMixin, viewsets.ModelViewSet):
    """docstring"""

    permission_classes = (permissions.IsAuthenticated, IsOwnerAndReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = InHospitalTransact.objects.all()
    serializer_class = InHospitalTransactSerializer
    filter_class = InHospitalTransactFilter
    search_fields = (
        'order_sn', 'trade_sn', 'open_time', 'transact_status',
        'transact_comments', 'pay_time',
        'next_order')
    ordering_fields = ('order_sn', 'trade_sn', 'open_time', 'pay_time')
