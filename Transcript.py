import json
from Course import Course

class Transcript:
    def __init__(self, course_list, given_credit, completed_credit, point, gano):
        self.course_list = course_list
        self.given_credit = given_credit
        self.completed_credit = completed_credit
        self.point = point
        self.gano = gano