from django.dispatch import receiver
from django.db.models.signals import pre_save


from .models import TransHospitalTransact


@receiver(pre_save, sender= TransHospitalTransact)
def NotifyPractitioner(sender, **kwargs):
    if "instance" in kwargs:
        inst=kwargs.get("instance")
        print(inst.order_sn)
        if inst.transact_status == 'TRANS_ACCEPTED':
            inst.PatientRecord.prescribe_practitioner = inst.to_practitioner.user
            inst.PatientRecord.save()
        # # APN_token is needed here.!!!!!!
        # device = APNSDevice.objects.get(registration_id= 'yzx') # to the from_practitioner
        # device.send_message(message={"title": "Transfer Request", "body": "A new patient has been transferred to you!"},
        #                 extra={"foo": "bar"})
        
        elif inst.transact_status == 'CLOSED':
            pass
        # # APN_token is needed here.!!!!!!
        # device = APNSDevice.objects.get(registration_id= 'yzx') # to the from_practitioner
        # device.send_message(message={"title": "Transfer Request", "body": "Transfer Closed"},
        #                 extra={"foo": "bar"})
        elif inst.transact_status == 'WAITING_ACCEPTED':
            pass
        # # APN_token is needed here.!!!!!!
        # device = APNSDevice.objects.get(registration_id= 'yzx') # to the to_practitioner
        # device.send_message(message={"title": "Transfer Request", "body": "Transfer Closed"},
        #                 extra={"foo": "bar"})
