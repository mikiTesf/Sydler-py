import random
import sys

from sydler.utils.role import Role
from sydler.utils.assignment import Assignment
from sydler.data.member import Member


class Populate:

    def __init__(self, total_days):
        self.__program_dates = total_days
        self.__all_members = Member.select()
        if len(self.__all_members) == 0:
            sys.exit('no members found in the database\nexiting...')
        self.__assignment_queue = []
        self.__BEST = 2.0
        self.__NORMAL = 1.0
        self.__LEAST = 0.0

    def populate_role(self, _role):
        id_rank_pair = dict()

        for _date in self.__program_dates:
            if (_role == Role.SECOND_HALL) and self.is_sunday(_date):
                continue
            for _member in self.__all_members:
                if _role == Role.STAGE:
                    var_qualify = self.qualify(_member.can_be_stage)
                elif _role == Role.SECOND_HALL:
                    var_qualify = self.qualify(_member.can_assist_2nd_hall)
                else:  # _role is mic rotation
                    var_qualify = self.qualify(_member.can_rotate_mic)

                var_occupied = self.is_occupied(_member.id, _role, _date)
                var_role_exception = self.__BEST

                if _role == Role.STAGE:
                    var_role_exception = self.has_exception(_member.has_sunday_exception, _date)

                var_distance = self.distance(_member.id)
                var_appearance_before = self.number_of_times_before(_member.id)
                var_appearance_today = self.number_of_times_today(_member.id, _date)

                id_rank_pair[_member.id] = self.rank(
                    var_qualify,
                    var_occupied,
                    var_role_exception,
                    var_distance,
                    var_appearance_before,
                    var_appearance_today
                )
            chosen_member_id = self.get_highest_ranking_member(id_rank_pair)
            new_assignment = Assignment(chosen_member_id, _date, _role)
            self.__assignment_queue.append(new_assignment)

    def qualify(self, qualification):
        return self.__NORMAL if qualification else self.__LEAST

    def is_occupied(self, member_id, role, date):
        occupied = False

        for _assignment in self.__assignment_queue:
            if (_assignment.assignee_id == member_id) and (_assignment.assignment_date == date):
                if role == Role.STAGE:
                    return self.__LEAST
                occupied = occupied or True

        return self.__BEST if not occupied else self.__NORMAL

    def has_exception(self, has_exception, _date):
        # in Python's datetime class the 6th weekday is Sunday
        if self.is_sunday(_date) and has_exception:
            return self.__NORMAL
        return self.__BEST

    def distance(self, member_id):
        # the farthest possible date at which a member can be assigned on
        # is outside of the queue (an ideal convention to give a member the
        # maximum attainable rank)
        maximum_distance = len(self.__assignment_queue) + 1
        distance = 0
        member_id_found = False

        for index in range(len(self.__assignment_queue) - 1, -1, -1):
            distance += 1
            if self.__assignment_queue[index].assignee_id == member_id:
                member_id_found = True
                break

        return distance if member_id_found else maximum_distance

    def number_of_times_before(self, member_id):
        count = 0
        for _assignment in self.__assignment_queue:
            if _assignment.assignee_id == member_id:
                count += 1
        return count

    def number_of_times_today(self, member_id, _date):
        count = 0

        for _assignment in self.__assignment_queue:
            if (_assignment.assignee_id == member_id) and (_assignment.assignment_date == _date):
                count += 1
        return count

    @staticmethod
    def rank(qualify, occupied, role_exception, distance, appearance_before, appearance_today):
        numerator = qualify * occupied * role_exception * distance
        denominator = (appearance_before + 1) * (appearance_today + 1)
        return numerator / denominator

    @staticmethod
    def get_highest_ranking_member(id_rank_pair):
        max_rank = max(id_rank_pair.values())
        # there could be multiple members with the same max_rank
        chosen_member_ids = []

        for member_id in id_rank_pair.keys():
            if id_rank_pair[member_id] == max_rank:
                chosen_member_ids.append(member_id)

        random.shuffle(chosen_member_ids)
        # even after shuffling the possible candidates list, a random choice is
        # made from among the candidates(makes the process even more random)
        return random.choice(chosen_member_ids)

    @staticmethod
    def is_sunday(_date_):
        return _date_.isoweekday() == 7

    def get_assignments(self):
        for _role in Role.get_roles():
            self.populate_role(_role)
        return self.__assignment_queue
