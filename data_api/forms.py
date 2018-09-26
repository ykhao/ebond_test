import django_filters

from .models import (Patient, Practitioner, Hospital, PractitionerMembership,
                     MedicalRecord, DiagnosticReport,
                     Observation)


class NullFilter(django_filters.BooleanFilter):
    """
    NullFilter Class serves for backlog unattributed objects
    ------------------------------
    """

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.field_name: value})
        return qs


class PatientFilter(django_filters.FilterSet):
    """docstring for TaskFilter"""

    class Meta:
        model = Patient
        fields = ('id_no', 'name', 'gender', 'telecom', 'birth_date', 'address')


class PractitionerFilter(django_filters.FilterSet):
    """docstring for SprintFilter"""

    class Meta:
        model = Practitioner
        fields = (
            'id_no',
            'user',
            'name',
            'telecom',
            'qualification_id',
            'qualification_period',
            'qualification_issuer',
        )


class HospitalFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields = ('id_no', 'name', 'telecom', 'practitioners',
                  'qualification_level')


class PractitionerMembershipFilter(django_filters.FilterSet):
    class Meta:
        model = PractitionerMembership
        fields = ('hospital', 'practitioner', 'date_joined', 'relationship')


class MedicalRecordFilter(django_filters.FilterSet):
    class Meta:
        model = MedicalRecord
        fields = (
            'serial_no',
            'initial_date',
            'update_date',
            'patient',
            'prescribe_practitioner',
            'prescribe_comments',
        )


class DiagnosticReportFilter(django_filters.FilterSet):
    """docstring for """

    class Meta:
        model = DiagnosticReport
        fields = (
            'serial_no',
            'name',
            'patient',
            'practitioner',
            'comments',
        )


class ObservationFilter(django_filters.FilterSet):
    """docstring for """

    class Meta:
        model = Observation
        fields = (
            'name',
            'result',
            'diagnostic_report',
        )
