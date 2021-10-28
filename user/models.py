from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.


class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'admin'
        verbose_name = '账户'
        verbose_name_plural = verbose_name


class UserInfo(BaseModel):
    '''用户信息'''
    GENDER = (
        (1, 'male'),
        (0, 'female')
    )
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='电话', default=0)
    gender = models.SmallIntegerField(choices=GENDER, default=1, verbose_name='性别')
    family = models.ForeignKey('Family', verbose_name='所属家庭', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class ManufacturerInfo(BaseModel):
    '''用户信息'''
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='联系电话')
    city = models.CharField(max_length=30, verbose_name='城市')
    address = models.CharField(max_length=100, verbose_name='地址')

    class Meta:
        db_table = 'manufacturer_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Family(BaseModel):
    address = models.CharField(max_length=100, verbose_name='地址')
    num_of_user = models.IntegerField(default=0, verbose_name='家庭人数')
    zip_code = models.IntegerField(verbose_name='邮政编码')
    area = models.FloatField(verbose_name='面积')
    address = models.CharField(max_length=100, verbose_name='房屋种类')
    at_home = models.SmallIntegerField(default=1, verbose_name='是否在家')

    class Meta:
        db_table = 'family'
        verbose_name = '家庭信息'
        verbose_name_plural = verbose_name
