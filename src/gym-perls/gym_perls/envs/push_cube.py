from .perls_env import PerlsEnv
from lib.utils.math_util import euler2quat
import numpy as np

class PushCube(PerlsEnv):

    """
    Trying to solve InverseKinematics by RL
    """
    metadata = {
        'render.modes': ['human', 'depth', 'segment'],
        'video.frames_per_second': 50
    }

    def __init__(self, conf_path):

        super(PushCube, self).__init__(conf_path)
        self._cube = self._world.body['cube_0']
        self._robot = self._world.tool['m0']

    def _reset(self):

        super(PushCube, self)._reset()

        # move robot to initial position
        self._robot.reach(pos=[-0.45032182335853577, 0.0994880199432373, -0.16887788474559784], 
                          orn=euler2quat([np.pi / 2.0, 0.0, 0.0]))

        # TODO: should this be pinpoint???

        # TODO: set cube's initial position here

        return self._get_relative_pose()

    def _get_relative_pose(self):

        cube_pose_rel = self._cube.get_pose(self._robot.uid, 0)
        eef_pose_rel = self._robot.tool_pose_rel

        return eef_pose_rel, cube_pose_rel

    def _step(self, action):

        # TODO: action should be delta Robot end effector 2D pose, so do bounds clipping and apply action

        # TODO: make sure to go through IK here, since it's not perfect

        # TODO: then read robot state, and get the stuff we care about again. 

        return NotImplemented
