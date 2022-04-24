from Events.Game.move.algos.GameObjects.tools.point import Point
import math
from Events.Game.move.distance import get_2d_distance


def get_transform_between_points(source:Point, target:Point):
	transform = Point(target.x - source.x, target.y - source.y)

	return transform


def dec_to_rad(angle):
	return (3.14/180)*angle




def get_angle_between_points(point1:Point,point:Point,source_of_angle:Point):
	c=get_2d_distance(point1,point)
	b=get_2d_distance(source_of_angle,point1)
	a=get_2d_distance(source_of_angle,point)

	cos_alpha=(a**2+b**2-c**2)/(2.0*a*b)
	alpha=math.acos(cos_alpha)
	alpha_deg=math.degrees(alpha)
	if alpha_deg<0:
		raise Exception()
	return math.degrees(alpha)
