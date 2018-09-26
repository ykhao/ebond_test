from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'transhospitaltransact', views.TransHospitalTransactViewSet,
                base_name='transhospitaltransact')
router.register(r'inhospitaltransact', views.InHospitalTransactViewSet)

