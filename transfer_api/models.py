# @Author: HpMa
# @date: 2018-08-10
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.crypto import string2md5
from data_api.models import Patient, Practitioner, Hospital, MedicalRecord
from multiselectfield import MultiSelectField


def upload_dir_path(instance, filename):
    name, ext = filename.rsplit('.', maxsplit=1)
    path = instance.category()
    path += '/{}/{}.{}'.format(instance.md5salt(), name, ext)
    return path


class TransactBaseClass(models.Model):
    """
    TransactBaseClass | Interface
    ------------------------------
    """

    def placeholder(self):
        return None

    class Meta:
        abstract = True


class TransHospitalTransact(TransactBaseClass):
    # registered -- time excess closed(TEC.)
    #            |
    #         prescribed -- TEC
    #               |
    #       trans hospital initial --> TEC
    #                             |
    #                          waiting accepted --> accepted time excess
    #                               |
    #                           trans accepted --> closed(对于没有完全接入的医院）
    #                                   |
    #                              new order initial
    #                                       |
    #                                     closed（完全接入的医院）
    TREAT_STATUS = (
        ('REGISTERED', _('已挂号')),
        ('TIME_EXCESS_CLOSED', _('超时关闭')),
        ('PRESCRIBE', _('医生申请转诊')),
        ('TRANS_HOSPITAL_INITIAL', _('启动转诊')),
        ('WAITING_ACCEPTED', _('等待接收')),
        ('TRANS_ACCEPTED', _('转诊接收')),
        ('NEW_ORDER_INITIAL', _('上级医院转诊启动')),
        ('ACCEPTED_TIME_EXCESS', '接受时间超时'),
        ('CLOSED', _('转诊结束'))
    )

    from_hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, verbose_name='来源医院',
        related_name='from_hospital')
    to_hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, verbose_name='去向医院',
        related_name='to_hospital')
    from_practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, verbose_name='来源医生',
        related_name='from_practitioner')
    to_practitioner = models.ForeignKey(
        Practitioner, on_delete=models.CASCADE, verbose_name='去向医生',
        related_name='to_practitioner')
    PatientRecord = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, null=True, verbose_name='病人情况')
    order_sn = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name='检查单序列号')
    trade_sn = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name='转诊单序列号')
    open_time = models.DateTimeField(default=datetime.now, verbose_name='开始时间')
    transact_status = models.CharField(
        choices=TREAT_STATUS,
        default='REGISTERED',
        max_length=30,
        verbose_name='订单状态')
    transact_comments = models.TextField(
        max_length=500, default='', verbose_name='留言')
    pay_time = models.DateTimeField(default=datetime.now, verbose_name='支付时间')
    
    def __str__(self):
        return self.order_sn or _('ID is %s') % self.id

    def category(self):
        return  _('TransHospitalTransact')

class InHospitalTransact(TransactBaseClass):
    # registered -- time excess closed(TEC.)
    #            |
    #         prescribe&unpaid -- TEC
    #                          |
    #                          paid -- TEC
    #                               |
    #                           treatment
    #                                   |
    #                                 treatment success
    #                                       |
    #                                     closed
    TREAT_STATUS = (('REGISTERED', _('已挂号')),
                    ('TIME_EXCESS_CLOSED', _('超时关闭')), ('PRESCRIBE_UNPAID',
                                                        _('处方、未支付')),
                    ('PAID', _('已支付')), ('TREATMENT',
                                         _('治疗')), ('TREATMENT_FINISHED',
                                                    _('治疗结束')), ('CLOSED',
                                                                 _('诊疗结束')))

    # user =
    order_sn = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name='检查单序列号')
    trade_sn = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name='检查序列号')
    open_time = models.DateTimeField(default=datetime.now, verbose_name='开始时间')
    transact_status = models.CharField(
        choices=TREAT_STATUS,
        default='REGISTERED',
        max_length=30,
        verbose_name='订单状态')
    transact_comments = models.TextField(
        max_length=500, default='', verbose_name='留言')
    pay_time = models.DateTimeField(default=datetime.now, verbose_name='支付时间')
    next_order = models.ForeignKey(
        TransHospitalTransact, on_delete=models.CASCADE, verbose_name='次级订单')
    # next_order = models.CharField(default='', verbose_name='次级订单', max_length=100)
