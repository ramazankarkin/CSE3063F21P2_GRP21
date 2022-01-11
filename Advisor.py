class Advisor:
    def __init__(self, advisor_name, department, rank):
        self.advisor_name = advisor_name
        self.department = department
        self.rank = rank
        self.student_list = []
        self.quota_error_list = []
        self.prerequisite_error_list = []
        self.collision_error_list = []
        self.te_error_list = []
        self.project_error_list = []
        self.stu = {'Name': self.advisor_name, 'Department': self.department, 'Rank': self.rank}
