from django.db import models
from db.base_model import BaseModel


# Create your models here.

class Data(BaseModel):
    '''门窗信息'''
    device = models.ForeignKey('device.Device', verbose_name='所属设备', on_delete=models.CASCADE)
    data = models.FloatField(verbose_name='数据')
    type = models.CharField(max_length=30, verbose_name="数据类别")

    class Meta:
        db_table = 'data'
        verbose_name = '数据信息'
        verbose_name_plural = verbose_name


class Home(BaseModel):
    '''家庭数据展示'''
    humidity = models.FloatField(verbose_name='湿度')
    temperature = models.FloatField(verbose_name='温度')
    distance = models.FloatField(verbose_name='距离')
    foggy = models.SmallIntegerField(verbose_name='雾气')
    rain = models.SmallIntegerField(verbose_name='下雨')
    earthquake = models.SmallIntegerField(verbose_name='震动')
    lightness = models.SmallIntegerField(verbose_name='亮度')
    door = models.SmallIntegerField(verbose_name='门', default=1)
    window = models.SmallIntegerField(verbose_name='窗', default=1)


    class Meta:
        db_table = 'home'
        verbose_name = '家庭数据展示'
        verbose_name_plural = verbose_name



