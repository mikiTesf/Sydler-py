

class Assignment:

    def __init__(self, member_id, date_time, role):
        self.assignee_id = member_id
        self.role = role
        self.assignment_date = date_time

    # def __eq__(self, other):
    #     same_member_id = self.assignee_id == other.assignee_id
    #     same_role = self.role == other.role
    #     same_date = self.assignment_date == other.assignment_id
    #
    #     return same_member_id and same_date
