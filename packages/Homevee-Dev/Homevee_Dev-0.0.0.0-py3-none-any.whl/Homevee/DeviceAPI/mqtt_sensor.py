#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Utils.Database import Database


def handle_mqtt_sensor(device_id, value, db):

		cur = db.cursor()

		cur.execute("SELECT * FROM MQTT_SENSORS WHERE ID = :id", {'id': device_id})
		item = cur.fetchone()

		#if(item['LAST_VALUE'] != value):
			#trigger automation

		Database.update("UPDATE MQTT_SENSORS SET LAST_VALUE = :val WHERE ID = :id",
		{'val': value, 'id': device_id})

	#check if device is used in automation rules
