from enum import IntEnum

class Command(IntEnum):
    WALK = 0,
    LOOK = 1,


    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


    @classmethod
    def get_value(cls, value):
        return cls._value2member_map_[value]
