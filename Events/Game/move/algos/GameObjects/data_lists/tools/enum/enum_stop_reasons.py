from enum import Enum


class Reason_to_stop(Enum):
    ENERGY = "ENERGY"
    ONE_UAV_KILLED="one uav has been killed"
    TIME="time"
    POINTS_LIMIT="points limit reached"
    EXPLOITATION="exploitation"
    ITERATIONS="iterations"
    MINIMUM_TEMPERATURE="minimum temperature"
    NO_PROGRESS="no progress"
    NOT_ACCEPT_TRESH="not_accept_tresh"


