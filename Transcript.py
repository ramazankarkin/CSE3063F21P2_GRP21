import json
from Course import Course


class Transcript:
    def __init__(self, course_list, attended_credit, completed_credit, point, gano):
        self.course_list = course_list
        self.attended_credit = attended_credit
        self.completed_credit = completed_credit
        self.point = point
        self.gano = gano

    def json_dumps_text(self):
        data = []

        for course in self.course_list:
            data.append([course[0].json_dumps_text(), course[1]])  # This works if your fields have the same names.

        return {'Course List': data, 'Attended Credit': self.attended_credit,
                'Completed Credit': self.completed_credit, 'Point': self.point, 'GANO': self.gano}

    def get_course_list_without_grades(self):
        course_list_without_grades = []

        for course in self.course_list:
            course_list_without_grades.append(course[0])

        return course_list_without_grades
