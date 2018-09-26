from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import (Patient, Practitioner, Hospital, PractitionerMembership,
                     MedicalRecord, DiagnosticReport, Observation, )


class PatientSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = Patient
        fields = ('id', 'name', 'id_type', 'id_no',
                  'telecom',
                  'gender',
                  'spouse_name',
                  'spouse_id_type',
                  'spouse_id_no',
                  'spouse_telecom',
                  'birth_date',
                  'address',
                  'photo',
                  'contact_relationship',
                  'contact_name',
                  'contact_telecom',
                  'contact_gender',
                  'contact_address',
                  'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
                reverse('patients-detail', kwargs={'pk': obj.pk},
                        request=request)
        }


class PractitionerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Practitioner
        fields = (
            'url',
            'id',
            'user',
            'name',
            'id_no',
            'telecom',
            'qualification_id',
            'qualification_issuer',
            'qualification_period',
            'photo',
        )


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hospital
        fields = (
            'url',
            'id',
            'id_no',
            'name',
            'telecom',
            'qualification_level',
            'photo',
        )


class PractitionerMembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PractitionerMembership
        fields = (
            'url',
            'id',
            'practitioner',
            'hospital',
            'date_joined',
            'relationship',
        )


class MedicalRecordSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = MedicalRecord
        fields = (
            'links',
            'id',
            'serial_no',
            'initial_date',
            'update_date',
            'patient',
            'prescribe_practitioner',
            'prescribe_comments',
            'append_file',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
                reverse(
                    'MedicalRecord-detail',
                    kwargs={'pk': obj.pk},
                    request=request)
        }


class ObservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Observation
        fields = (
            'url',
            'id',
            'diagnostic_report',
            'name',
            'result',
        )


class DiagnosticReportSerializer(serializers.ModelSerializer):
    observations = ObservationSerializer(many=True, read_only=True)
    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = DiagnosticReport
        fields = (
            'links',
            'id',
            'serial_no',
            'name',
            'patient',
            'practitioner',
            'observations',
            'medical_record',
            'comments',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
                reverse(
                    'diagnosticreport-detail',
                    kwargs={'pk': obj.pk},
                    request=request)
        }
