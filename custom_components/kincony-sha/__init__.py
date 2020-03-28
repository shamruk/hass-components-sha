#!/usr/bin/python
import getopt
import socket
import sys
import re
import time
import os
import subprocess
import logging
import threading

DATA_DEVICE_REGISTER = "k_device_register"
DATA_DEVICE_REGISTER_LOCK = "k_device_register_lock"

_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel(logging.DEBUG)

default_ip = '192.168.1.103'

async def async_setup(hass, config):
	_LOGGER.info("k init")
	hass.data[DATA_DEVICE_REGISTER] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hass.data[DATA_DEVICE_REGISTER_LOCK] = threading.Lock()
	return True

class KConnection(object):
	def __init__(self, s, index, lock):
		super(KConnection, self).__init__()
		self.s = s
		self.index = index
		self.lock = lock
		
	def send2K(self, action_type):
		first_run = False
		fix_every_time = False
		kcode = '255'
		address = (default_ip, 4196)

		try:
			self.s.connect(address)
		except:
			_LOGGER.debug("cannot connect socket")

		if first_run:
			self.s.sendto('RELAY-SCAN_DEVICE-NOW'.encode(), address)
			result = self.s.recv(1024).decode('utf-8')
			_LOGGER.info("scan:" + result)

		if first_run or fix_every_time:
			self.s.sendto('RELAY-TEST-NOW'.encode(), address)
			result = self.s.recv(1024).decode('utf-8')
			_LOGGER.info("test:" + result)

		if action_type == 'on' and self.index == 'all':
			command = 'RELAY-SET_ALL-' + kcode + ',255'
		elif action_type == 'off' and self.index == 'all':
			command = 'RELAY-SET_ALL-' + kcode + ',0'
		elif action_type == 'on':
			command = 'RELAY-SET-' + kcode + ',' + self.index + ',1'
		elif action_type == 'off':
			command = 'RELAY-SET-' + kcode + ',' + self.index + ',0'
		elif action_type == 'get':
			command = 'RELAY-READ-' + kcode + ',' + self.index
		elif action_type == 'test':
			command = 'RELAY-TEST-NOW'
		elif action_type == 'scan':
			command = 'RELAY-SCAN_DEVICE-NOW'
		elif action_type == 'error':
			command = 'zzz'

		self.s.sendto(command.encode(), address)
		result = self.s.recv(1024).decode('utf-8')

		# self.s.close()

		_LOGGER.debug("request:" + command)
		_LOGGER.debug("response:" + result)

		return result

	def send2KWithLock(self, action_type):
		with self.lock:
			result = self.send2K(action_type)
		return result

	def turnOn(self):
		result = self.send2KWithLock('on')
		x = re.match("RELAY-SET-\\d+,\\d+,(\\d+),OK", result)
		if x.group(1) != "1":
			_LOGGER.warning("exit 5")


	def turnOff(self):
		result = self.send2KWithLock(action_type)
		x = re.match("RELAY-SET-\\d+,\\d+,(\\d+),OK", result)
		if x.group(1) != "0":
			_LOGGER.warning("exit 6")	

	def getStatus(self):
		result = self.send2KWithLock(action_type)
		x = re.match("RELAY-READ-\\d+,\\d+,(\\d+),OK", result)
		return x.group(1) == "1"
