from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.

class Device(BaseModel):
    '''设备信息'''
    category = models.ForeignKey('Category', verbose_name='所属种类', on_delete=models.CASCADE)
    family = models.ForeignKey('user.Family', verbose_name='所属家庭', on_delete=models.CASCADE)
    manufacture = models.ForeignKey('user.User', verbose_name='所属制造商', on_delete=models.CASCADE)
    name = models.CharField(max_length=45, verbose_name='姓名')
    description = models.CharField(max_length=100, verbose_name='描述')
    place = models.CharField(max_length=30, verbose_name='产地')

    class Meta:
        db_table = 'device'
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name

class Category(BaseModel):
    '''种类信息'''
    name = models.CharField(max_length=45, verbose_name='种类名称')

    class Meta:
        db_table = 'category'
        verbose_name = '种类'
        verbose_name_plural = verbose_name



