class Course:
    def __init__(self, course_name, course_credit,
                 semester, quota, prerequisite, elective_type, course_hour):
        self.course_name = course_name
        self.number_of_student = 0
        self.course_credit = course_credit
        self.semester = semester
        self.quota = quota
        self.prerequisite = prerequisite
        self.elective_type = elective_type
        self.course_hour = course_hour

    def json_dumps_text(self):
        if self.elective_type is not None:
            return {'Course Name': self.course_name, 'Course Credit': self.course_credit,
                    'Quota': self.quota, 'Prerequisite': self.prerequisite,
                    'Elective Type': self.elective_type}
        else:
            return {'Course Name': self.course_name, 'Course Credit': self.course_credit,
                    'Semester': self.semester, 'Prerequisite': self.prerequisite}
