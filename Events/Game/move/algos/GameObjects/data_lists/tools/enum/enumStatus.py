from enum import Enum


class UavStatus(Enum):

    TIER_0=1
    TIER_1=2
    TIER_2=3
    WAIT=4
    ON_WAY=5
    ON_ATTACK=6
    ON_BACK=7
    ON_TEMP_BACK=8
    DEAD=9
    VISUALISE=10
    DODGE=11
    BACK_FROM_DODGE=12
    PLANED_DODGE=13
    ATTACK_DODGE_MOVE=14


    def to_string(self):
        if self==self.ON_BACK:
            return "On back"
        elif self==self.TIER_1:
            return "TIER_1"
        elif self == self.TIER_2:
            return "TIER_2"
        elif self == self.WAIT:
            return "WAIT"
        elif self == self.ON_ATTACK:
            return "ON_ATTACK"
        elif self == self.ON_TEMP_BACK:
            return "On temp back"
        elif self ==self.DEAD:
            return "DEAD"
        else:
            return "Status nieznany"

class HandStatus(Enum):
    CHASING=0
    TIER_0=1
    DEFENCE=3
    BACK=2
    WAIT=4
    JUMP=5
    WAIT_AFTER_JUMP=6


class Sides(Enum):
    RIGHT=0
    LEFT=1
