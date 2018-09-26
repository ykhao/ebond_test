from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from utils.permissions import IsOwner, IsOwnerAndReadOnly
from .forms import (PatientFilter, PractitionerFilter, HospitalFilter,
                    PractitionerMembershipFilter, MedicalRecordFilter,
                    DiagnosticReportFilter,
                    ObservationFilter)
from .models import (Patient, Practitioner, Hospital, PractitionerMembership,
                     MedicalRecord, DiagnosticReport,
                     Observation)
from .serializers import (PatientSerializer, PractitionerSerializer,
                          HospitalSerializer, PractitionerMembershipSerializer,
                          MedicalRecordSerializer,
                          DiagnosticReportSerializer, ObservationSerializer)


class DefaultMixin(object):
    """
    Default views settings, to be successed by other viewsets.
    """
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class PatientViewSet(DefaultMixin, viewsets.ModelViewSet):
    """
    get:
    Return a list of exist patients

    post:
    Add a new patient to list
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)

    # queryset = Patient.objects.order_by('birth_date')
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        practitioner = self.request.user
        queryset1 = MedicalRecord.objects.filter(
            prescribe_practitioner=practitioner)
        pats=list(queryset1)
        queryset=Patient.objects.filter(id=-1)
        for MdR in pats:
            queryset = queryset.union(Patient.objects.filter(id=MdR.patient.id))
        return queryset

    filter_class = PatientFilter
    search_fields = ('name',)
    ordering_fields = (
        'birth_date',
        'name',
    )


class PractitionerViewSet(DefaultMixin, viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    filter_class = PractitionerFilter
    search_fields = ('name',)
    ordering_fields = ('qualification_period', 'name')


class HospitalViewSet(DefaultMixin, viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_class = HospitalFilter
    search_fields = ('id_no', 'name', 'qualification_level')
    ordering_fields = ('qualification_level')


class PractitionerMembershipViewSet(DefaultMixin, viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = PractitionerMembership.objects.all()
    serializer_class = PractitionerMembershipSerializer
    filter_class = PractitionerMembershipFilter
    search_fields = ('practitioner', 'hospital', 'date_joined', 'relationship')
    ordering_fields = ('date_joined', 'relationship')


class MedicalRecordViewSet(DefaultMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerAndReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)

    #queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        user=self.request.user
        querytset=MedicalRecord.objects.filter(prescribe_practitioner=user)
        return querytset

    # @action(detail=False, methods=['GET'])
    # def get_related_patients(self, pk=None):
    #     practitioner = self.request.user
    #     patients = MedicalRecord.objects.filter(
    #         prescribe_practitioner=practitioner).patient
    #     return PatientSerializer(patients).data

    filter_class = MedicalRecordFilter
    search_fields = ('patient', 'initial_date', 'update_date')
    ordering_fields = ('update_date', 'initial_date')
    # @action(detail=True, methods=['PATCH'])
    # def prescribe_practitioner(self, request, *args, **kwargs):
    #     medical_record = self.get_object()
    #     next_prescribe_practitioner = request.data['prescribe_practitioner']
    #     serializer = MedicalRecordSerializer(medical_record,
    #                                          data=next_prescribe_practitioner)
    #     if serializer.is_valid():
    #         medical_record.prescribe_practitioner_set.add(serializer)
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class DiagnosticReportViewSet(DefaultMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerAndReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = DiagnosticReport.objects.all()
    serializer_class = DiagnosticReportSerializer
    filter_class = DiagnosticReportFilter
    search_fields = ('serial_no', 'patient', 'practitioner')
    ordering_fields = ('serial_no')


class ObservationViewSet(DefaultMixin, viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    filter_class = ObservationFilter
    search_fields = ('name')
    ordering_fields = ('name', 'result')
