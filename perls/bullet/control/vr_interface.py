from bullet.control.interface import CtrlInterface
import pybullet as p
import time
import redis

class IVR(CtrlInterface):

	# TODO: reset signal, pass controller IDs, add configuration file system

	def __init__(self, host, remote):
		# Default settings for camera
		super(IVR, self).__init__(host, remote)

	def event_callback(self, model, vr):

		# if not self.server.connected:
		# 	self.server.connect()
		model.reset(0, vr)
		p.setRealTimeSimulation(0)
		control_map = model.create_control_mappings()

		revert_map = {key: {v: k for k, v in val.items()} for key, val in control_map.items()}
		def _cmd_handler(msg):

			packet = msg['data']
			if isinstance(packet, str) or isinstance(packet, bytes):
				data = eval(packet)
				if data == 0:
					raise SystemExit('Remote client invoke shut down')
				elif data == 1:
					print('Remote client invode reset')
					model.reset(0, vr)
					p.setRealTimeSimulation(0)
				else:
					for obj, pose in data.items():
						if obj not in model.grippers:

							p.resetBasePositionAndOrientation(obj, pose[0], pose[1])
						else:
							# Change the gripper constraint if obj is pr2 gripper
							p.changeConstraint(control_map[2][revert_map[1][obj]], pose[0], pose[1], maxForce=500)

				# TODO: Handle constraints of grippers; 
				# Handle joint states

		self.server.pubsub.subscribe(**{'client_channel': _cmd_handler})
		self.server.pubsub.run_in_thread(sleep_time=0.001)

		# Ctrl, running in different thread
		while True:
			events = p.getVREvents()
			for e in (events):
				r.publish('server_channel', e)
				time.sleep(0.001)

	def _remote_comm(self, model):
		tool = model.get_tool_ids()
		model.set_virtual_controller([3, 4])
		
		self.server.connect(model)

		control_map = model.create_control_mappings()

		while True:
			if model.controllers:
				events = self.server.read_msg()

				skip_flag = model.redundant_control()

				for e in (events):
					if skip_flag:
						if e[0] == model.controllers[1]:
							break
						model.control(e, control_map)
					else:
						model.control(e, control_map)


				msg = {}
				for ID in range(p.getNumBodies()):
					msg[ID] = p.getBasePositionAndOrientation(ID)[:2]
				self.server.broadcast_msg(msg)

	def _local_comm(self, model):
		control_map = model.create_control_mappings()
		while True:
			events = p.getVREvents()
			skip_flag = model.redundant_control()
			for e in (events):
				if skip_flag:
					if e[0] == model.controllers[1]:
						break
					model.control(e, control_map)
				else:
					model.control(e, control_map)

	


