from enum import Enum


class Role(Enum):
    STAGE = 0
    MIC_ROUND_1_LEFT = 1
    MIC_ROUND_1_RIGHT = 2
    MIC_ROUND_2_LEFT = 3
    MIC_ROUND_2_RIGHT = 4
    SECOND_HALL = 5

    @staticmethod
    def get_roles():
        return (
            Role.STAGE,
            Role.MIC_ROUND_1_LEFT,
            Role.MIC_ROUND_1_RIGHT,
            Role.MIC_ROUND_2_LEFT,
            Role.MIC_ROUND_2_RIGHT,
            Role.SECOND_HALL)
