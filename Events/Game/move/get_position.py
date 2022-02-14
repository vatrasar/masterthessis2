import math
from random import Random

from Events.Game.move.GameObjects.tools.geometry import get_transform_between_points
from Events.Game.move.GameObjects.tools.point import Point


def get_point_on_tier1(current_position:Point,distance,target_position:Point):
	new_point=Point(0,current_position.y)
	if current_position.x-target_position.x<0:
		new_point.x=current_position.x+distance
	else:
		new_point.x=current_position.x-distance

	return new_point


def get_random_position_on_tier1(rand:Random,map_width,tier1_distance):

    x=(map_width)*rand.random()

    return Point(x,tier1_distance)


def get_vector_with_length_and_direction(distance,direction_vector:Point):
	try:
		sum_of_squares=direction_vector.x**2+direction_vector.y**2

		scale_factor=distance/math.sqrt(sum_of_squares)
		result=Point(direction_vector.x,direction_vector.y)
		result.x=result.x*scale_factor
		result.y=result.y*scale_factor

		return result
	except ZeroDivisionError:
		print("Bląąąąąąąąąąd")

def get_point_based_on_time(current_position:Point,time,target_position:Point,velocity):
	distance=time*velocity
	transofrm_between_points=get_transform_between_points(current_position,target_position)
	direction_vector=get_vector_with_length_and_direction(distance,transofrm_between_points)
	new_postion=Point(current_position.x+direction_vector.x,current_position.y+direction_vector.y)
	return new_postion

def get_point_base_on_distance(current_position:Point, distance, target_position:Point):
	transofrm_between_points=get_transform_between_points(current_position,target_position)
	direction_vector=get_vector_with_length_and_direction(distance,transofrm_between_points)
	new_postion=Point(current_position.x+direction_vector.x,current_position.y+direction_vector.y)
	return new_postion
