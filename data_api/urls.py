from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'patients', views.PatientViewSet, base_name="patients")
router.register(r'practitioners', views.PractitionerViewSet)
router.register(r'hospital', views.HospitalViewSet)
router.register(r'practitionermembership', views.PractitionerMembershipViewSet)
router.register(r'medical_record', views.MedicalRecordViewSet, base_name="MedicalRecord")
router.register(r'observation', views.ObservationViewSet)
router.register(r'diagnosticreport', views.DiagnosticReportViewSet)
