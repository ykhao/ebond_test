from django.contrib import admin
from .models import (Patient, Practitioner, Hospital, PractitionerMembership,
                     MedicalRecord, Observation,
                     DiagnosticReport)
from transfer_api.models import TransHospitalTransact, InHospitalTransact
from auth_api.models import UserProfile


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'id_no', 'telecom', 'gender', 'birth_date', 'address',
        'photo', 'contact_relationship', 'contact_name',
        'contact_telecom', 'contact_gender', 'contact_address')


class PractitionerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'id_no', 'name', 'telecom', 'qualification_id',
        'qualification_period', 'qualification_issuer')


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'id_no',  'telecom',
                    'qualification_level')


class PractitionerMembershipAdmin(admin.ModelAdmin):
    pass


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'initial_date', 'update_date')


class ObservationInline(admin.StackedInline):
    model = Observation
    extra = 1


class ObservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'result',
        'diagnostic_report',
    )


class DiagnosticReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serial_no',
        'name',
        'patient',
        'practitioner',
        'comments',
    )
    inlines = [ObservationInline]


class TransHospitalTransactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'from_hospital', 'to_hospital','from_practitioner', 'to_practitioner', 'PatientRecord', 'order_sn', 'trade_sn', 'open_time',
        'transact_status', 'pay_time'
    )


class InHospitalTransactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_sn', 'trade_sn', 'open_time', 'transact_status',
        'transact_comments', 'pay_time', 'next_order'
    )


admin.site.register(Patient, PatientAdmin)
admin.site.register(Practitioner, PractitionerAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(PractitionerMembership, PractitionerMembershipAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(TransHospitalTransact, TransHospitalTransactAdmin)
admin.site.register(InHospitalTransact, InHospitalTransactAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(DiagnosticReport, DiagnosticReportAdmin)
