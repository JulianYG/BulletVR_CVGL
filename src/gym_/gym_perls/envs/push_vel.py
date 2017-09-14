# !/usr/bin/env python

from .push_cube import PushCube
from lib.utils import math_util


class PushCubeVel(PushCube):
    """
    Pushing cube across the table
    """
    def __init__(self, conf_path):

        super(PushCubeVel, self).__init__(conf_path)

    @property
    def observation_space(self):

        table_bound, table_orn = self._table.pose

        table_abs_upper_bound = table_bound + math_util.vec((.325, .2, 0.))
        table_abs_lower_bound = table_bound - math_util.vec((.325, .2, 0.))

        table_upper = math_util.get_relative_pose(
            (table_abs_upper_bound, table_orn), self._robot.pose)
        table_lower = math_util.get_relative_pose(
            (table_abs_lower_bound, table_orn), self._robot.pose)

        goal_abs_lower = math_util.vec((cube.pos[0] + 0.25, cube.pos[1] - 0.25, 0.641))
        goal_abs_upper = math_util.vec((cube.pos[0] + 0.45, cube.pos[1] + 0.25, 0.642))

        goal_upper = math_util.get_relative_pose(
            (goal_abs_upper, table_orn), self._robot.pose)
        goal_lower = math_util.get_relative_pose(
            (goal_abs_lower, table_orn), self._robot.pose)

        return PushCube.Space.Box(
            low=math_util.concat((
                math_util.vec(self._robot.joint_specs['lower']),
                -math_util.vec(self._robot.joint_specs['max_vel']),
                table_lower,
                (-1, -1, -1, -1),
                goal_lower)
            ),
            high=math_util.concat((
                math_util.vec(self._robot.joint_specs['upper']),
                math_util.vec(self._robot.joint_specs['max_vel']),
                table_upper,
                (1, 1, 1, 1),
                goal_upper)
            )
        )

    @property
    def action_space(self):
        return PushCube.Space.Box(
            low=-math_util.vec(self._robot.joint_specs['max_vel']),
            high=math_util.vec(self._robot.joint_specs['max_vel'])
        )

    def _step_helper(self, action):
        # Use velocity control
        self._robot.joint_velocities = action
