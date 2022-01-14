from Transcript import Transcript
import logging


class Advisor:
    def __init__(self, advisor_name, department, rank):
        self.advisor_name = advisor_name
        self.department = department
        self.rank = rank
        self.student_list = []
        self.quota_error_list = []
        self.prerequisite_error_list = []
        self.collision_error_list = []
        self.collision_error_list = []
        self.te_error_list = []
        self.project_error_list = []
        self.stu = {'Name': self.advisor_name, 'Department': self.department, 'Rank': self.rank}

    def add_approval_courses(self):
        for student in self.student_list:
            attended_credit = student.transcript_before.attended_credit
            my_transcript_after = []

            for course in student.course_offered:
                if course.elective_type == "TE" and student.transcript_before.completed_credit < 155:
                    error = "The advisor didnt approve TE - " + course.course_name + " because student completed credits less than 155"
                    student.errors.append(error)
                    if student.student_number not in self.te_error_list:
                        self.te_error_list.append(student.student_number)
                        logging.warning(student.student_number + " - " + error)  # will print a message to the console

                elif (course.course_name == "Engineering Project I" or course.course_name == "Engineering Project II") and student.transcript_before.completed_credit < 165:
                    error = "The advisor didnt approve " + course.course_name + " because student completed credits less than 165"
                    student.errors.append(error)
                    if student.student_number not in self.project_error_list:
                        self.project_error_list.append(student.student_number)
                        logging.warning(student.student_number + " - " + error)  # will print a message to the console

                else:
                    my_transcript_after.append([course, None])
                    attended_credit += course.course_credit

            my_transcript_after = student.transcript_before.course_list + my_transcript_after

            student.transcript_after = Transcript(my_transcript_after, attended_credit,
                                                  student.transcript_before.completed_credit,
                                                  student.transcript_before.point, student.transcript_before.gano)