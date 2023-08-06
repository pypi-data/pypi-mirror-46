#
# Edbot Software API Python module.
#

import json
import threading
import http.client
import urllib.parse
import getpass
import time

from ws4py.client.threadedclient import WebSocketClient

class EdbotClient(WebSocketClient):
	def __init__(self, server="localhost", port=8080, client="Python"):
		self.client = client
		self.server = server
		self.port = port
		self.auth = "AUTH_NONE"
		self.data = {}
		self.connected = False
		self.ready_event = threading.Event()
		self.active_event = {}
		self.motion_seq = 0
		self.motion_busy = {}
		self.motion_event = {}
		self.speech_seq = 0
		self.speech_busy = {}
		self.speech_event = {}
		self.callback = None

	###########################################################################
	#
	# Common functions.
	#
	###########################################################################

	def connect(self, callback=None):
		if self.connected:
			raise Exception("Already connected to server")
		self.callback = callback
		url = "ws://" + self.server + ":" + str(self.port) + "/api/reporter/" + \
			self.enc(getpass.getuser()) + "/" + self.enc(self.client) + "/3"
		WebSocketClient.__init__(self, url)
		WebSocketClient.connect(self)
		t = threading.Thread(target=self.run_forever)
		t.setDaemon(True)
		t.start()
		self.ready_event.wait()

	def get_connected(self):
		return self.connected

	def disconnect(self):
		if not self.connected:
			raise Exception("Not connected to server")
		WebSocketClient.close(self, code=1000, reason="Closed by client")

	def get_robot_names(self, model=None):
		if not self.connected:
			raise Exception("Not connected to server")
		if model is None:
			return list(self.data["robots"].keys())
		else:
			result = []
			for name in self.data["robots"].keys():
				if self.data["robots"][name]["model"]["key"] == model:
					result.append(name)
			return result

	def get_robot(self, name):
		if not self.connected:
			raise Exception("Not connected to server")
		if not name in self.data["robots"]:
			raise Exception(name + " is not configured on this server")
		else:
			return self.data["robots"][name]

	def get_data(self):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.data

	def is_active(self, name):
		if not self.connected:
			raise Exception("Not connected to server")
		robot = self.get_robot(name)
		if not robot["activeUser"] is None:
			return robot["activeUser"] == self.data["user"]
		return True

	def wait_until_active(self, name):
		if not self.connected:
			raise Exception("Not connected to server")
		if not self.is_active(name):
			self.active_event[name] = threading.Event()
			# Don't use the more efficient wait() - it isn't interruptible.
			while not self.active_event[name].is_set():
				time.sleep(0.1)

	def get_remote_servers(self):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("remote_servers", all=True)

	def set_servo_torque(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_torque/" + self.enc(name) + "/" + path)

	def set_servo_speed(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_speed/" + self.enc(name) + "/" + path)

	def set_servo_position(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_position/" + self.enc(name) + "/" + path)

	def say(self, name, text, wait=True, speech_seq=None):
		if not self.connected:
			raise Exception("Not connected to server")
		if speech_seq is None:
			self.speech_seq += 1
			speech_seq_str = self.auth + "_s_" + str(self.speech_seq)
		else:
			speech_seq_str = self.auth + "_self_s_" + str(speech_seq)
		#
		# Check if we are waiting for this Edbot to finish speaking. If so, wait.
		# This could happen in a multi-threaded environment :-)
		#
		if name in self.speech_event.keys():
			self.speech_event[name].wait()
		params = { "busy": speech_seq_str }
		if wait == False:
			return self.api_request("say/" + self.enc(name) + "/" + self.enc(text), params)
		else:
			self.speech_busy[name] = speech_seq_str
			self.speech_event[name] = threading.Event()
			resp = self.api_request("say/" + self.enc(name) + "/" + self.enc(text), params)
			if resp["success"] == True:
				self.speech_event[name].wait()
			else:
				self.speech_event[name].set()
			return resp

	def reset(self, name):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("reset/" + self.enc(name))

	def set_options(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("options/" + self.enc(name) + "/" + path)

	###########################################################################
	#
	# Edbot functions.
	#
	###########################################################################

	def get_motions(self, name):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("motions/" + self.enc(name), all=True)

	def get_default_motions(self, model):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("def_motions/" + self.enc(model), all=True)

	def run_motion(self, name, motion, wait=True, motion_seq=None):
		if not self.connected:
			raise Exception("Not connected to server")
		if motion_seq is None:
			self.motion_seq += 1
			motion_seq_str = self.auth + "_m_" + str(self.motion_seq)
		else:
			motion_seq_str = self.auth + "_self_m_" + str(motion_seq)
		#
		# Check if we are waiting for this Edbot to finish a motion. If so, wait.
		# This could happen in a multi-threaded environment :-)
		#
		if name in self.motion_event.keys():
			self.motion_event[name].wait()
		params = { "busy": motion_seq_str }
		if wait == False:
			return self.api_request("motion/" + self.enc(name) + "/" + str(motion), params)
		else:
			self.motion_busy[name] = motion_seq_str
			self.motion_event[name] = threading.Event()
			resp = self.api_request("motion/" + self.enc(name) + "/" + str(motion), params)
			if resp["success"] == True:
				self.motion_event[name].wait()
			else:
				self.motion_event[name].set()
			return resp

	def set_servo_led(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_led/" + self.enc(name) + "/" + path)

	def set_servo_pid(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_pid/" + self.enc(name) + "/" + path)

	###########################################################################
	#
	# Edbot Dream functions.
	#
	###########################################################################

	def set_servo_mode(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_mode/" + self.enc(name) + "/" + path)

	def set_servo_combined(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("servo_combined/" + self.enc(name) + "/" + path)

	def set_buzzer(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("buzzer/" + self.enc(name) + "/" + path)	

	def set_custom(self, name, path):
		if not self.connected:
			raise Exception("Not connected to server")
		return self.api_request("custom/" + self.enc(name) + "/" + path)

	###########################################################################
	#
	# Private.
	#
	###########################################################################

	def opened(self):
		self.connected = True

	def closed(self, code, reason=None):
		# Stop waiting.
		for name in self.active_event:
			self.active_event[name].set()
		for name in self.motion_busy:
			self.motion_event[name].set()
		for name in self.speech_busy:
			self.speech_event[name].set()
		self.ready_event.set()

		# Reset status.
		self.connected = False
		self.auth = "AUTH_NONE"
		self.data = {}

	def received_message(self, m):
		msg = json.loads(m.data.decode("UTF-8"))
		self.data = self.dict_merge(self.data, msg)
		if "initComplete" in self.data.keys():
			self.ready_event.set()
		if "auth" in self.data.keys():
			self.auth = self.data["auth"]
		if "robots" in self.data.keys():
			for name in self.data["robots"].keys():
				robot = self.data["robots"][name]
				if "activeUser" in robot.keys():
					if robot["activeUser"] is None or robot["activeUser"] == self.data["user"]:
						try:
							self.active_event[name].set()
						except:
							pass
				if "connected" in robot.keys():
					if robot["connected"] == True:
						try:
							if robot["reporters"]["motionComplete"] == self.motion_busy[name]:
								self.motion_event[name].set()
						except:
							pass
						try:
							if robot["reporters"]["speechComplete"] == self.speech_busy[name]:
								self.speech_event[name].set()
						except:
							pass
					else:
						if name in self.motion_event:
							self.motion_event[name].set()
						if name in self.speech_event:
							self.speech_event[name].set()
		if self.callback is not None:
			self.callback(msg)

	def api_request(self, path, params=None, all=None):
		url = "/api/" + path
		if params is not None:
			url = url + "?" + urllib.parse.urlencode(params)
		conn = http.client.HTTPConnection(self.server, self.port)
		conn.request("GET", url, headers = { "X-Edbot-Auth" : self.auth })
		response = conn.getresponse()
		data = response.read()
		conn.close()
		dic = json.loads(data.decode("UTF-8"))
		if all is not None and all:
			return dic
		else:
			return dic["status"]

	def enc(self, str, safe=""):
		return urllib.parse.quote(str, safe)

	def dict_merge(self, target, *args):
		# Merge multiple dicts.
		if len(args) > 1:
			for obj in args:
				self.dict_merge(target, obj)
			return target

		# Recursively merge dicts and set non-dict values.
		obj = args[0]
		if not isinstance(obj, dict):
			return obj
		for k, v in obj.items():
			if v is None:
				target[k] = None
			elif k in target and isinstance(target[k], dict):
				self.dict_merge(target[k], v)
			else:
				target[k] = v
		return target