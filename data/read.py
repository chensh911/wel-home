#!/usr/bin/python
# -*- coding: utf-8 -*

import paho.mqtt.client as mqtt
import json
import pymysql
import time

from django.shortcuts import render

from data.models import Home

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('mathilda33/emqx')


# 消息接收回调
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    sqlsave(json.loads(msg.payload))
    client.disconnect()


def main_demo():
    client = mqtt.Client()

    # 指定回调函数
    client.on_connect = on_connect
    client.on_message = on_message

    # 建立连接
    client.connect('broker.emqx.io', 1883, 60)
    # 发布消息
    # client.publish('emqtt', payload='Hello World', qos=0)

    client.loop_forever()



# MySQL保存
def sqlsave(jsonData):
    # 打开数据库连接
    home = Home.objects.get(id=1)
    home.humidity = jsonData['hum']
    home.temperature = jsonData['temp']
    # home.distance = jsonData['distance']
    # home.foggy = jsonData['foggy']
    # home.rain = jsonData['rain']
    # home.earthquake = jsonData['earthquake']
    home.lightness = jsonData['led']
    home.door = jsonData['door']
    home.window = jsonData['window']

    home.save()

def publish_data(type, data):
    client = mqtt.Client()
    # 指定回调函数
    client.on_connect = on_connect
    print(type, data)
    # 建立连接
    client.connect('broker.emqx.io', 1883, 60)
    # 发布消息
    client.publish(type, payload=data, qos=0)

if __name__ == '__main__':
    main_demo()
