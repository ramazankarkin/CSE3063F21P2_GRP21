import json
from Advisor import Advisor
from Transcript import Transcript


class Student:
    def __init__(self, student_number, student_name, year, advisor, transcript_before, course_offered):
        self.student_number = student_number
        self.student_name = student_name
        self.year = year
        self.advisor = advisor
        self.transcript_before = transcript_before
        self.course_offered = course_offered
        self.transcript_after = []
        self.errors = []

    def json_dumps_text(self):
        course_offered_text = []

        for course in self.course_offered:
            course_offered_text.append(course.json_dumps_text())

        return {'Student Number': self.student_number, 'Student Name': self.student_name, 'Year': self.year,
                'Advisor': self.advisor.stu, 'Transcript Before': self.transcript_before.json_dumps_text(),
                'Course Offered': course_offered_text, 'Transcript After': self.transcript_after.json_dumps_text(), 'Errors': self.errors}

    def toJSON(self):
        with open("students/" + str(self.student_number) + ".json", "w", encoding="utf-8") as outfile:
            json_for_student = json.dumps(self.json_dumps_text(), ensure_ascii=False, default=lambda o: o.__dict__,
                                          indent=4)
            outfile.write(json_for_student)
