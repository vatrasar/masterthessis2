from Events.Game.move.GameObjects.tools.point import Point


def get_transform_between_points(source:Point, target:Point):
	transform = Point(target.x - source.x, target.y - source.y)

	return transform




