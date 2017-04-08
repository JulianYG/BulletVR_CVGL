import pybullet as p


class Scene(object):
	"""
	The basic scene setup in VR 
	"""
	def __init__(self, enableForceSensor):
		"""
		Other subclasses may re-implement the constructor
		"""		
		self.BUTTONS = 6
		self.ORIENTATION = 2
		self.controllers = None
		self.obj_cnt = 0

		self.hand = False
		self.grippers = []
		self.constraints = []
		self.arms = []
		self.VR_HAND_ID = None

		self.has_force_sensor = enableForceSensor

	def reset(self, flag):
		"""
		Load task for both recording and replay
		"""
		try:
			# Use GUI and turn off simulation for replay
			if flag:
				p.connect(p.GUI)
				p.setRealTimeSimulation(0)
				# In order to generate deterministic paths
			else:
				p.connect(p.SHARED_MEMORY)
				p.setRealTimeSimulation(1)
			
			p.setInternalSimFlags(0)
			# convenient for video recording
		
		except p.error:
			return 0
		self.controllers = [e[0] for e in p.getVREvents()]
		self.create_scene()
		return 1

	def create_scene(self):
		raise NotImplementedError("Each VR Setup must re-implement this method.")

	def control(self, event, ctrl_map):
		raise NotImplementedError("Each VR Setup must re-implement this method.")

	def get_arm_ids(self):
		return self.arms

	def set_time_step(self, time_step):
		p.setTimeStep(time_step)

	def step_simulation(self, time_step):
		p.stepSimulation()

	def set_force_sensor(self):
		self.has_force_sensor = True

	def create_control_mappings(self):
		control_map = {}
		if self.grippers:
			control_map['gripper'] = dict(zip(self.controllers, self.grippers))
		if self.arms:
			control_map['arm'] = dict(zip(self.controllers, self.arms))
		if self.constraints:
			control_map['constraint'] = dict(zip(self.controllers, self.constraints))
		return control_map

	def is_unicontrol(self):
		return len(self.controllers) > max(len(self.grippers), len(self.arms), len(self.constraints))

	def load_task(self, task):
		# May implement differently in grasping task for labels
		for obj in task:
			p.loadURDF(*obj)
		self.obj_cnt = p.getNumBodies()

	def load_basic_env(self):

		p.setGravity(0, 0, -9.81)
		p.loadURDF("plane.urdf",0,0,0,0,0,0,1)
		p.loadURDF("table/table.urdf", 1.1, -0.2, 0., 0., 0., 0.707107, 0.707107)


	def load_default_env(self):

		p.loadURDF("plane.urdf", 0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,1.000000)
		p.loadURDF("jenga/jenga.urdf", 1.300000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("jenga/jenga.urdf", 1.200000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("jenga/jenga.urdf", 1.100000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("jenga/jenga.urdf", 1.000000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("jenga/jenga.urdf", 0.900000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("jenga/jenga.urdf", 0.800000,-0.700000,0.750000,0.000000,0.707107,0.000000,0.707107)
		p.loadURDF("table/table.urdf", 1.000000,-0.200000,0.000000,0.000000,0.000000,0.707107,0.707107)
		p.loadURDF("teddy_vhacd.urdf", 1.050000,-0.500000,0.700000,0.000000,0.000000,0.707107,0.707107)
		p.loadURDF("cube_small.urdf", 0.950000,-0.100000,0.700000,0.000000,0.000000,0.707107,0.707107)
		p.loadURDF("sphere_small.urdf", 0.850000,-0.400000,0.700000,0.000000,0.000000,0.707107,0.707107)
		p.loadURDF("duck_vhacd.urdf", 0.850000,-0.400000,0.900000,0.000000,0.000000,0.707107,0.707107)
		p.loadURDF("teddy_vhacd.urdf", -0.100000,-2.200000,0.850000,0.000000,0.000000,0.000000,1.000000)
		p.loadURDF("sphere_small.urdf", -0.100000,-2.255006,1.169706,0.633232,-0.000000,-0.000000,0.773962)
		p.loadURDF("cube_small.urdf", 0.300000,-2.100000,0.850000,0.000000,0.000000,0.000000,1.000000)
		p.loadURDF("table_square/table_square.urdf", -1.000000,0.000000,0.000000,0.000000,0.000000,0.000000,1.000000)
		shelf = p.loadSDF("kiva_shelf/model.sdf")[0]
		p.resetBasePositionAndOrientation(shelf, [-0.700000,-2.200000,1.204500],[0.000000,0.000000,0.000000,1.000000])
		p.setGravity(0, 0, -9.81)



		