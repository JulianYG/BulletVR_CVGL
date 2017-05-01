import pybullet as p
from bullet.utils.enum import *

class IllegalOperation(Exception):
	def __init__(self, link):
		self.link = link

def illegal_operation_handler(e, comm):
	print('Captured client\'s illegal operation. Notifying client')
	comm.broadcast_to_client(
		(WARNING_HOOK, 
			[
			'Warning: you are flipping arm link {}. Positions reset'.format(e.link),
			(1.7, 0, 1), (255, 0, 0), 12, 1.5
			]
		)
	)

def task_monitor_handler(comm):
	print('Client completed one task')
	comm.broadcast_to_client(
		(WARNING_HOOK, 
		['Good job! You completed one piece of task',
		(1.7, 0, 1), (255, 0, 0), 12, 5])
	)


	