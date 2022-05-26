from enum import Enum


class Reason_to_stop(Enum):
    ONE_UAV_KILLED="one uav has been killed"
    TIME="time"
    POINTS_LIMIT="points limit reached"
    EXPLOITATION="exploitation"
    ITERATIONS="iterations"
    MINIMUM_TEMPERATURE="minimum temperature"
    NO_PROGRESS="no progress"

