import math
from random import Random

import numpy as np

from Events.Game.move.GameObjects.tools.point import Point


def get_2d_distance(source, position):
	x_target=position.x
	y_target=position.y
	x_source=source.x
	y_source=source.y


	p1 = np.array([x_target, y_target])
	p2 = np.array([x_source, y_source])

	squared_dist = np.sum((p1 - p2) ** 2, axis=0)
	dist = np.sqrt(squared_dist)

	return dist


def get_horizontal_distance(current_postion:Point, target_postion:Point):
	if current_postion.x-target_postion.x<0:
		return target_postion.x-current_postion.x
	else:
		return current_postion.x-target_postion.x


def get_vector_with_direction_and_length(dircetion:Point,length):
	power=math.sqrt(dircetion.x**2 +dircetion.y**2)
	unit_vector=Point(dircetion.x/power,dircetion.y/power)
	result_vcetor=Point(unit_vector.x*length,unit_vector.y)

	return result_vcetor
