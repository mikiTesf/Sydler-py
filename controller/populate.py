import random

from data import db_connection
from controller import role
from controller import assignment


class Populate:

    def __init__(self, total_days):
        self.__program_dates = total_days
        self.__all_members = db_connection.DBConnection.get_all_members()
        self.__assignment_queue = []
        self.__BEST = 2.0
        self.__NORMAL = 1.0
        self.__LEAST = 0.0

    def populate_role(self, _role):
        id_rank_pair = dict()

        for _date in self.__program_dates:
            for member in self.__all_members:
                var_qualify = True
                var_role_exception = False

                if role is role.Role.STAGE:
                    var_qualify = self.qualify(member.can_be_stage())
                if role is role.Role.MIC:
                    var_qualify = self.qualify(member.can_rotate_mic())
                if role is role.Role.SECOND_HALL:
                    var_qualify = self.qualify(member.can_assist_2nd_hall())

                var_occupied = self.is_occupied(member.ID, _role)

                if _role == role.Role.STAGE:
                    var_role_exception = self.has_exception(member.excep)

                var_distance = self.distance(member.ID)
                var_appearance_before = self.number_of_times_before(member.ID)
                var_appearance_today = self.number_of_times_today(member.ID)

                id_rank_pair[member.ID] = Populate.rank(
                    var_qualify,
                    var_occupied,
                    var_role_exception,
                    var_distance,
                    var_appearance_before,
                    var_appearance_today
                )
                new_assignment = assignment.Assignment(member.ID, _date, _role)
                self.__assignment_queue.append(new_assignment)
        return None

    def qualify(self, qualification):
        if qualification:
            return self.__NORMAL
        return self.__LEAST

    def is_occupied(self, member_id, _role_):
        occupied = False

        for _assignment in self.__assignment_queue:
            if _assignment.assignee_id == member_id:
                if _role_ == role.Role.STAGE:
                    return self.__LEAST
                occupied = occupied or True

        return self.__BEST if not occupied else self.__NORMAL

    def has_exception(self, has_exception):
        if has_exception:
            return self.__NORMAL
        return self.__BEST

    def distance(self, member_id):
        # the farthest possible date at which a member can be assigned on
        # is outside of the queue (an ideal convention to give a member the
        # maximum attainable rank)
        maximum_distance = len(self.__assignment_queue) + 1
        distance = maximum_distance
        member_id_found = False

        for index in range(len(self.__assignment_queue), -1, -1):
            if self.__assignment_queue[index].assignee_id == member_id:
                member_id_found = True
                distance += 1
        return distance if member_id_found else maximum_distance

    def number_of_times_before(self, member_id):
        count = 0
        for _assignment in self.__assignment_queue:
            if _assignment.assignee_id == member_id:
                count += 1
        return count

    def number_of_times_today(self, member_id):
        count = 0

        for _assignment in self.__assignment_queue:
            if _assignment.assignee_id == member_id:
                count += 1
        return count

    @staticmethod
    def rank(qualify, occupied, role_exception, distance, appearance_before, appearance_today):
        return (qualify * occupied * role_exception) * distance / ((appearance_before + 1) * (appearance_today + 1))

    @staticmethod
    def get_highest_ranking_member(id_rank_pair):
        max_rank = max(id_rank_pair.values())
        # there could be multiple members with the same max_rank
        chosen_member_ids = []

        for member_id in id_rank_pair.keys():
            if id_rank_pair[member_id] == max_rank:
                chosen_member_ids.append(member_id)

        random.shuffle(chosen_member_ids)
        # even after shuffling the possible candidates list, a random
        # index using which a member will be chosen is generated (makes
        # the choosing process fairer)
        random_index = random.randint(len(chosen_member_ids))
        return chosen_member_ids[random_index]
