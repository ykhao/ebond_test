from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    id_no = models.TextField(
        verbose_name='ID_No', max_length=100, default='', null=False)
    name = models.TextField(
        verbose_name='Name', max_length=100, default='', null=False)
    telecom = models.CharField(
        verbose_name='Mobile phone', max_length=30, default='', null=False)

    '''
    qualification_id = models.TextField(
        verbose_name=_('证书编号'), blank=False, default='')
    qualification_period = models.DurationField(
        verbose_name=_('医生执照有效期'), blank=False, null=True)
    qualification_issuer = models.TextField(
        verbose_name=_('发证机构'), null=True, blank=True)
    '''

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
