from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import math

def get_zone_index(settings:Settings,x_position):
    zone_width=float(settings.map_size_x)/settings.naive_algo_list_limit
    zone_index=math.floor(x_position/zone_width)
    return zone_index