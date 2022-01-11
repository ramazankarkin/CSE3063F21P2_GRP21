import json
from Advisor import Advisor

class Student:
    def __init__(self, student_number, student_name, year, advisor, transcript_before, course_offered, errors):
        self.student_number = student_number
        self.student_name = student_name
        self.year = year
        self.advisor = advisor
        self.transcript_before = transcript_before
        self.course_offerd = course_offered
        self.errors = errors
        self.stu = {'Student Number':self.student_number,'Student Name' : self.student_name,'Year' : self.year,'Advisor' : self.advisor.stu}


    def createStudentJSON(self):
        with open("students/"+str(self.student_number)+ ".json", "w") as outfile:
            json_for_student = json.dumps(self.stu, indent=6)
            outfile.write(json_for_student)

    def toJSON(self):   
        with open("students/"+str(self.student_number)+ ".json", "w") as outfile:
            json_for_student = json.dumps(self.stu, default=lambda o: o.__dict__, indent=4)
            outfile.write(json_for_student)