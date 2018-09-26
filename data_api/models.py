# @Author: HpMa
# @date: 2018-08-08

from abc import abstractmethod

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.crypto import string2md5
from core2 import settings


def upload_dir_path(instance, filename):
    name, ext = filename.rsplit('.', maxsplit=1)
    path = instance.category()
    path += '/{}/{}.{}'.format(instance.md5salt(), name, ext)
    return path


class DataClass(object):
    """
    DataClass Interface
    ---------------
    2 method must be implemented for safety
    md5salt: return md5salt of an instance
    category: return the category of a class
    """

    @abstractmethod
    def md5salt(self):
        raise NotImplementedError

    @abstractmethod
    def category(self):
        raise NotImplementedError


class Patient(DataClass, models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = (
        (MALE, _('男')),
        (FEMALE, _('女')),
    )
    ID_CARD = '0'
    MILITARY_OFFICER_CARD = '1'
    PASSPORT = '2'
    HK_MO_PASS = '3'
    MTP = '4'
    ID_TYPE_CHOICES = (
        (ID_CARD, '身份证'),
        (MILITARY_OFFICER_CARD, '军官证'),
        (PASSPORT, '护照'),
        (HK_MO_PASS, '港澳通行证'),
        (MTP, '台胞证'),
    )
    '''
    Reverse reference:
    --------------------------------------------------
    .medical_records -->>  MedicalRecord
    .diagnostic_reports -->> DiagnosticReport
    .observations -->> Observations
    '''
    name = models.TextField(
        verbose_name=_('姓名'), max_length=20, default='', )
    id_type = models.CharField(
        verbose_name=_('证件类型'), max_length=1,
        choices=ID_TYPE_CHOICES,
        default=ID_CARD, null=True, blank=True, )
    id_no = models.TextField(
        verbose_name=_('证件号码'), max_length=20,
        default='', )
    telecom = models.CharField(
        verbose_name=_('手机号码'),
        max_length=20,
        default='', )
    gender = models.CharField(
        verbose_name=_('性别'), max_length=1,
        choices=GENDER_CHOICE, )
    spouse_name = models.TextField(
        verbose_name='配偶姓名', max_length=20,
        default='', )
    spouse_id_type = models.CharField(
        verbose_name='配偶证件类型', max_length=1,
        choices=ID_TYPE_CHOICES, default=ID_CARD,
        null=True, blank=True, )
    spouse_id_no = models.TextField(
        verbose_name=_('配偶证件号码'), max_length=20,
        default='', null=True,
        blank=True, )
    spouse_telecom = models.CharField(
        verbose_name=_('配偶手机号码'),
        max_length=20,
        default='', )
    birth_date = models.DateField(
        verbose_name=_('出生日期'), blank=True,
        null=True, )
    address = models.TextField(
        verbose_name=_('地址'), blank=True, null=True)
    photo = models.ImageField(
        verbose_name='照片', upload_to=upload_dir_path,
        blank=True,
        null=True, )
    contact_relationship = models.TextField(
        verbose_name=_('同患者关系'), max_length=10,
        blank=True, null=True, )
    contact_name = models.TextField(
        verbose_name=_('联系人姓名'), max_length=100, default='', blank=True,
        null=False, )
    contact_telecom = models.CharField(
        verbose_name=_('联系人手机号码'),
        max_length=30,
        default='',
        null=False, blank=True, )
    contact_gender = models.CharField(
        verbose_name=_('联系人性别'), max_length=1,
        choices=GENDER_CHOICE, blank=True, null=True, )
    contact_address = models.TextField(
        verbose_name=_('联系人地址'),
        blank=True, null=True, )

    def __str__(self):
        return self.name or _('ID is %s') % self.id

    def md5salt(self):
        return string2md5(str(self.id))

    def category(self):
        return _('Patient')


class Practitioner(DataClass, models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = (
        (MALE, _('man')),
        (FEMALE, _('woman')),
    )
    '''
    Reverse reference:
    --------------------------------------------------
    .medical_records -->>  MedicalRecord
    .diagnostic_reports -->> DiagnosticReport
    .observations -->> Observations
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.TextField(
        verbose_name=_('姓名'), max_length=100, default='', null=False)
    id_no = models.TextField(
        verbose_name=_('身份证号'), max_length=100, default='', null=False)
    telecom = models.CharField(
        verbose_name=_('手机号码'), max_length=30, default='', null=False)
    qualification_id = models.TextField(
        verbose_name=_('证书编号'), blank=False, default='')
    photo = models.ImageField(
        upload_to=upload_dir_path, blank=False, null=True)
    qualification_period = models.DurationField(
        verbose_name=_('医生执照有效期'), blank=False, null=True)
    qualification_issuer = models.TextField(
        verbose_name=_('发证机构'), null=True, blank=True)

    def __str__(self):
        return self.name or _('ID is %s') % self.id

    def md5salt(self):
        return string2md5(str(self.id))

    def category(self):
        return _('Practitioner')


class Hospital(DataClass, models.Model):
    QUALIFICATION_LEVEL = (
        ('A1', _('一甲')),
        ('A2', _('一乙')),
        ('A3', _('一丙')),
        ('B1', _('二甲')),
        ('B2', _('二乙')),
        ('B3', _('二丙')),
        ('C1', _('三甲')),
        ('C2', _('三乙')),
        ('C3', _('三丙')),
    )
    '''
    Reverse reference:
    --------------------------------------------------
    .practitioners -->> Practitioner
    .medical_records -->>  MedicalRecord
    .diagnostic_reports -->> DiagnosticReport
    .observations -->> Observations
    '''
    id_no = models.TextField(
        verbose_name=_('医院编号'), max_length=100, default='', null=False)
    name = models.TextField(
        verbose_name=_('医院名称'), max_length=100, default='', null=False)
    telecom = models.CharField(
        verbose_name=_('医院电话'), max_length=30, default='', null=False)
    practitioners = models.ManyToManyField(
        Practitioner, through='PractitionerMembership')
    qualification_level = models.CharField(
        verbose_name=_('医院资质'),
        choices=QUALIFICATION_LEVEL,
        blank=False,
        max_length=2,
        default='')
    photo = models.ImageField(
        upload_to=upload_dir_path, blank=True, null=True)

    def __str__(self):
        return self.id_no + ' ' + self.name

    def md5salt(self):
        return string2md5(str(self.id))

    def category(self):
        return _('Hospital')


class PractitionerMembership(models.Model):
    """
    PractitionerMembership serves for Practitioner <--> Hospital ManyToMany
    relationship
    """
    PRACTITIONER_HOSPITAL_RELATIONSHIP = (
        ('A', _('正式')),
        ('B', _('专家')),
        ('C', _('实习')),
    )
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date_joined = models.DateField()
    relationship = models.CharField(
        max_length=3, blank=False, choices=PRACTITIONER_HOSPITAL_RELATIONSHIP)

    def __str__(self):
        return self.hospital.name + ' ' + self.practitioner.name


class MedicalRecord(DataClass, models.Model):
    """
    Reverse reference:
    --------------------------------------------------
    .practitioners -->> Practitioner
    .medical_records -->>  MedicalRecord
    .diagnostic_reports -->> DiagnosticReport
    .observations -->> Observations
    """
    serial_no = models.CharField(
        verbose_name=_('序列号'), max_length=30, default='', null=False)
    initial_date = models.DateTimeField(verbose_name=_('入院时间'), blank=False,
                                        null=True)
    update_date = models.DateTimeField(verbose_name=_('病历更新时间'), blank=True,
                                       null=True)
    patient = models.ForeignKey(
        Patient,
        verbose_name=_('患者'),
        blank=False,
        null=False,
        related_name='medical_records',
        on_delete=models.CASCADE)
    prescribe_practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('主治医师'),
        related_name='medical_records',
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    prescribe_comments = models.TextField(verbose_name=_('处方'), default='')
    append_file = models.FileField(
        verbose_name=_('附件'),
        upload_to=upload_dir_path,
        blank=True,
        null=True)

    def __str__(self):
        return self.serial_no or _('Serial Number is %s') % self.serial_no

    def md5salt(self):
        return string2md5(str(self.serial_no))

    def category(self):
        return _('Medical Record')


# 要分开DiagnosticReport和这个报告中的每一个条目
# 因为检测项目在两个医院之间并不统一，如：血常规包含的项目、每一项的参考范围等都是
# 可变的，而且在与医院完全对接钱是不可预测的。
# 为了实现这一个数据模型可以容纳一切检测结果，需要把诊断报告和具体检测的细节分开处理。
# 在Observation中，通过外键指向DiagnosticReport以表明从属关系，
# 这样可以不用针对每一个检测项目（如血常规、尿常规等）都重新新建一张表，
# 让所有检测报告在一张表上，所有具体检测在一张表，让今后的拓展性更强。
class DiagnosticReport(DataClass, models.Model):
    """
    Reverse Reference
    ------------------------------
    .observations --> Observations
    """
    serial_no = models.CharField(
        verbose_name='序列号', max_length=30, default='', null=False)
    name = models.TextField(
        verbose_name='检测名称', max_length=100, default='', null=False)
    # reverse reference: patient.diagnostic_reports
    patient = models.ForeignKey(
        Patient,
        blank=False,
        null=False,
        related_name='diagnostic_reports',
        on_delete=models.CASCADE)
    # reverse reference: practitioner.diagnostic_reports
    practitioner = models.ForeignKey(
        Practitioner,
        blank=False,
        null=False,
        related_name='diagnostic_reports',
        on_delete=models.CASCADE)
    medical_record = models.ForeignKey(
        MedicalRecord,
        verbose_name=_('病历'),
        on_delete=models.CASCADE,
        blank=False)
    comments = models.TextField(max_length=500, default='', null=True)

    # Media
    def __str__(self):
        return self.serial_no or _('Serial Number is %s') % self.serial_no

    def md5salt(self):
        return string2md5(str(self.serial_no))

    def category(self):
        return _('Diagnostic Report')


class Observation(DataClass, models.Model):
    """
    Reverse Reference
    ------------------------------
    """
    name = models.TextField(blank=False, default="请填写")
    result = models.TextField(blank=True)

    # 此处不需要有指向患者的外键，因为通过患者直接查询检测条目是不可靠的，检测的时间、有效期、检测评价等等
    # 信息都在DiagnosticReport中，只能通过诊断报告找到对应的具体条目。
    # reverse reference: diagnostic_report.observations
    diagnostic_report = models.ForeignKey(
        DiagnosticReport,
        blank=False,
        related_name='observations',
        null=False,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name or _('Value is %s') % self.result

    def md5salt(self):
        return string2md5(str(self.pk))

    def category(self):
        return _('Observation')
