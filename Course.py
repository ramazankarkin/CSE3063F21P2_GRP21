class Course:
    def __init__(self, course_name, course_credit,
    semester, quota, prerequisite, elective_type, course_hour):
        self.course_name = course_name
        self.student_list = []
        self.course_credit = course_credit
        self.semester = semester
        self.quota = quota
        self.prerequisite = prerequisite
        self.elective_type = elective_type
        self.course_hour = course_hour