#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time

import paho.mqtt.client as mqtt

from juice.handler.extend.device.SysGpioHandler import *
from juice.handler.extend.device.SysPropHandler import *
from juice.model.JuiceMessage import JuiceMessage
from juice.util import Util

EVENT_CONNECT_KEY = "sys_connect"
EVENT_DISCONNECT_KEY = "sys_disconnect"
ID = "id"
TYPE = "type"
DATA = "data"
TIME = "time"

sys_handler_dict = {'sys_temp': SysTempGetHandler(), 'sys_volts': SysVoltsGetHandler(),
                    'sys_arm': SysArmGetHandler(), 'sys_gpu': SysGpuGetHandler()
    , 'gpio_get': GpioStatusGetHandler(), 'gpio_init': GpioInitHandler(), 'gpio_set': GpioSetHandler()
                    }


class MqttClient(object):

    def __init__(self, product_code, device_code, secret):
        self.product_code = product_code
        self.device_code = device_code
        self.secret = secret
        self.host = 'mqtt.juicecloud.cn'
        self.port = 2883
        self.prop_report_topic = "/{product_code}/{device_code}/prop/report".format(product_code=self.product_code,
                                                                                    device_code=self.device_code)
        self.prop_up_topic = "/{product_code}/{device_code}/prop/up".format(product_code=self.product_code,
                                                                            device_code=self.device_code)
        self.prop_down_topic = "/{product_code}/{device_code}/prop/down".format(product_code=self.product_code,
                                                                                device_code=self.device_code)
        self.task_up_topic = "/{product_code}/{device_code}/task/up".format(product_code=self.product_code,
                                                                            device_code=self.device_code)
        self.task_down_topic = "/{product_code}/{device_code}/task/down".format(product_code=self.product_code,
                                                                                device_code=self.device_code)
        self.sys_up_topic = "/{product_code}/{device_code}/sys/up".format(product_code=self.product_code,
                                                                          device_code=self.device_code)
        self.sys_down_topic = "/{product_code}/{device_code}/sys/down".format(product_code=self.product_code,
                                                                              device_code=self.device_code)
        self.prop_down_handler = None
        self.task_down_handler = None
        self.sys_down_handler = sys_handler_dict
        self.client = None

    def __str__(self):
        return "%s,%s,%s,%s,%s" % (self.product_code, self.device_code, self.secret,
                                   self.host, self.port)

    def __on_connect(self, client, userdata, flags, rc):
        message = {
            0: 'Connection successful',
            1: 'Connection refused - incorrect protocol',
            2: 'Connection refused - invalid client',
            3: 'Connection refused - server unavailable',
            4: 'Connection refused - bad username or password',
            5: 'Connection refused - not authorised'
        }
        print(message.get(rc, 'Currently unused'))
        self.client.publish(self.sys_up_topic, json.dumps(Util.get_raspberry_sys_info()), qos=0, retain=False)
        self.client.subscribe(self.sys_down_topic)
        print("Subscribe topic: " + self.sys_down_topic)
        self.client.subscribe(self.prop_down_topic)
        print("Subscribe topic: " + self.prop_down_topic)
        self.client.subscribe(self.task_down_topic)
        print("Subscribe topic: " + self.task_down_topic)

    def __on_message(self, client, userdata, msg):
        json_obj = json.loads(msg.payload.decode("utf-8"))
        print "%s: [topic]:[%s] [Received Message]:[%s]" % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), msg.topic, json_obj)
        if ID not in json_obj:
            print "message prop id not exist"
            return
        message_id = json_obj[ID]

        if TYPE in json_obj:
            type_key = json_obj[TYPE]
            message = JuiceMessage(type_key, json_obj.get(DATA, ''), json_obj.get(TIME, int(round(time.time() * 1000))))
            message.id = message_id
            if msg.topic == self.prop_down_topic and type_key in self.prop_down_handler.keys():
                self.prop_down_handler[type_key].execute(self, str(msg.topic), message)
            elif msg.topic == self.task_down_topic and type_key in self.task_down_handler.keys():
                self.task_down_handler[type_key].execute(self, str(msg.topic), message)
            elif msg.topic == self.sys_down_topic and type_key in self.sys_down_handler.keys():
                self.sys_down_handler[type_key].execute(self, str(msg.topic), message)
            else:
                print "%s handler not exist" % type_key
                return

    def __on_disconnect(self, client, userdata, rc):
        pass

    def __on_publish(self, client, userdata, mid):
        pass

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def __on_unsubscribe(self, client, userdata, mid):
        pass

    def __on_log(self, client, userdata, level, buf):
        pass

    def __init(self):
        client_id = self.device_code
        client = mqtt.Client('master-%s' % client_id)
        client.username_pw_set(self.device_code, self.secret)
        client.connect(self.host, self.port, 60)
        client.reconnect_delay_set(min_delay=1, max_delay=120)
        # client.on_connect = self.on_connect
        # client.on_message = self.on_message
        # client.on_disconnect = self.on_disconnect
        # client.on_publish = self.on_publish
        # client.on_subscribe = self.on_subscribe
        # client.on_unsubscribe = self.on_unsubscribe
        # client.on_log = self.on_log
        client.on_message = self.__on_message
        client.on_connect = self.__on_connect
        self.client = client

    def __subscriber(self):
        self.client.loop_forever()

    def prop_reply(self, message):
        print "%s: [topic]:[%s] [Send Message]:[%s]" % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.prop_up_topic, message)
        self.client.publish(self.prop_up_topic, str(message), qos=0, retain=False)

    def prop_reporter(self, message):
        print "%s: [topic]:[%s] [Send Message]:[%s]" % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.prop_report_topic, message)
        self.client.publish(self.prop_report_topic, str(message), qos=0, retain=False)

    def task_reply(self, message):
        print "%s: [topic]:[%s] [Send Message]:[%s]" % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.task_up_topic, message)
        self.client.publish(self.task_up_topic, str(message), qos=0, retain=False)

    def sys_reply(self, message):
        print "%s: [topic]:[%s] [Send Message]:[%s]" % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.sys_up_topic, message)
        self.client.publish(self.sys_up_topic, str(message), qos=0, retain=False)

    def init(self):
        self.__init()
        self.__subscriber()

    @property
    def prop_message(self):
        return self.prop_down_handler

    @prop_message.setter
    def prop_message(self, handler_dict):
        self.prop_down_handler = handler_dict

    @property
    def task_message(self):
        return self.task_down_handler

    @task_message.setter
    def task_message(self, handler_dict):
        self.task_down_handler = handler_dict
