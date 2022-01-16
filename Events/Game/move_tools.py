import numpy as np


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
