# import required packages
import json
import random
import glob
import logging
from random import randint
from Student import Student
from Advisor import Advisor
from Course import Course
from Transcript import Transcript


def get_create_new_student_from_json():
    json_file = open("input.json", encoding="utf-8")
    variables = json.load(json_file)
    json_file.close()

    return True if variables['createNewStudents'] is True else False


def get_semester_from_json():
    json_file = open("input.json", encoding="utf-8")
    variables = json.load(json_file)
    json_file.close()

    return variables['semester']


def get_advisors_from_json():
    json_file = open("input.json", encoding="utf-8")
    variables = json.load(json_file)
    json_file.close()

    my_advisor_list = []

    for advisor in variables['advisors']:
        new_advisor = Advisor(advisor['advisorName'], advisor['department'], advisor['rank'])
        my_advisor_list.append(new_advisor)

    return my_advisor_list


def create_courses():
    my_course_list = []

    for semester in range(1, 9):
        my_course_list += create_semester_courses(semester)

    my_course_list += create_elective_courses("NTE")
    my_course_list += create_elective_courses("ENG-UE")
    my_course_list += create_elective_courses("TE")
    my_course_list += create_elective_courses("ENG-FTE")

    return my_course_list


def create_semester_courses(semester):
    json_file = open("input.json", encoding="utf-8")
    variables = json.load(json_file)
    json_file.close()

    my_course_list = []

    for courses in variables['courses']:
        for semester_course in courses[str(semester)]:
            new_course = Course(semester_course['courseName'], semester_course['courseCredit'],
                                semester, None, None, None, semester_course['courseHourCode'])

            if 'prerequisite' in semester_course:
                new_course.prerequisite = semester_course['prerequisite']

            my_course_list.append(new_course)

    return my_course_list


def create_elective_courses(electiveType):
    json_file = open("input.json", encoding="utf-8")
    variables = json.load(json_file)
    json_file.close()

    my_course_list = []

    for courses in variables['courses']:
        for elective in courses[electiveType]:
            new_course = Course(elective['courseName'], elective['courseCredit'],
                                None, elective['quota'], None, electiveType, elective['courseHourCode'])

            if 'prerequisite' in elective:
                new_course.prerequisite = elective['prerequisite']

            my_course_list.append(new_course)

    return my_course_list


def get_semester_courses(semester):
    my_course_list = []

    for course in course_list:
        if course.semester == semester:
            my_course_list.append(course)

    return my_course_list


def get_elective_courses(elective_type):
    my_course_list = []

    for course in course_list:
        if course.elective_type == elective_type:
            my_course_list.append(course)

    return my_course_list


def initialize_students():
    if get_create_new_student_from_json():
        for year in range(1, 5):
            advisor = advisor_list[randint(0, len(advisor_list) - 1)]
            random_student = list(range(70))
            random.shuffle(random_student)
            for student_count in random_student:
                student = Student(generate_student_number(year, student_count), generate_random_name(), year, advisor,
                                  create_transcript(year), None)
                student.course_offered = create_course_offered(student)
                student_list.append(student)
                advisor.student_list.append(student)
        print("• {} students were recreated.\n".format(len(student_list)))
    else:
        files = glob.glob('students/*', recursive=True)
        for single_file in files:
            with open(single_file, encoding="utf-8") as f:
                data = json.load(f)
                new_student = Student(data['Student Number'], data['Student Name'],
                                      data['Year'], data['Advisor'],
                                      data['Transcript Before'], data['Course Offered'])
                student_list.append(new_student)
        print("• Action was taken on {} existing students.".format(len(student_list)))


def create_transcript(year):
    my_course_list = []
    point = 0
    attended_credit = 0
    completed_credit = 0

    for semester in range(1, semester_to_int(year)):
        for course in get_semester_courses(semester):
            letter_grade = generate_random_letter_grade()
            my_course_list.append([course, letter_grade])

            attended_credit += course.course_credit
            point += course.course_credit * get_numeric_grade_from_letter_grade(letter_grade)

            if letter_grade != "FF" and letter_grade != "FD":
                completed_credit += course.course_credit

        if semester == 2:
            while True:
                course = get_elective_courses("NTE")[randint(0, len(get_elective_courses("NTE")) - 1)]
                if my_course_list.count(course) == 0:
                    letter_grade = generate_random_letter_grade()
                    my_course_list.append([course, letter_grade])
                    attended_credit += course.course_credit
                    point += course.course_credit * get_numeric_grade_from_letter_grade(letter_grade)
                    if letter_grade != "FF" and letter_grade != "FD":
                        completed_credit += course.course_credit
                    break

        elif semester == 7:
            while True:
                course = get_elective_courses("TE")[randint(0, len(get_elective_courses("TE")) - 1)]
                if my_course_list.count(course) == 0:
                    letter_grade = generate_random_letter_grade()
                    my_course_list.append([course, letter_grade])
                    attended_credit += course.course_credit
                    point += course.course_credit * get_numeric_grade_from_letter_grade(letter_grade)
                    if letter_grade != "FF" and letter_grade != "FD":
                        completed_credit += course.course_credit
                    break

            while True:
                course = get_elective_courses("ENG-UE")[randint(0, len(get_elective_courses("ENG-UE")) - 1)]
                if my_course_list.count(course) == 0:
                    letter_grade = generate_random_letter_grade()
                    my_course_list.append([course, letter_grade])
                    attended_credit += course.course_credit
                    point += course.course_credit * get_numeric_grade_from_letter_grade(letter_grade)
                    if letter_grade != "FF" and letter_grade != "FD":
                        completed_credit += course.course_credit
                    break

    gano = round(point / attended_credit, 2) if attended_credit != 0 else 0.0
    transcript = Transcript(my_course_list, attended_credit, completed_credit, point, gano)
    return transcript


def create_course_offered(student):
    my_course_list = []
    total_course_list = student.transcript_before.get_course_list_without_grades()
    semester_int = semester_to_int(student.year)
    semester_courses = get_semester_courses(semester_int)

    for course in semester_courses:
        my_course_list.append(course)
        total_course_list.append(course)
        course.number_of_student += 1
        for transcript_courses in student.transcript_before.course_list:
            if (course.prerequisite == transcript_courses[0].course_name and
                    (transcript_courses[1] == "FF" or transcript_courses[1] == "FD")):
                error = "The system did not allow " + course.course_name + " because student failed prerequisite " + course.prerequisite;
                student.errors.append(error)
                my_course_list.pop()
                total_course_list.pop()

                if student.student_number not in student.advisor.prerequisite_error_list:
                    student.advisor.prerequisite_error_list.append(student.student_number)

    nte_courses = get_elective_courses("NTE")
    te_courses = get_elective_courses("TE")
    ue_courses = get_elective_courses("ENG-UE")
    fte_courses = get_elective_courses("ENG-FTE")

    if semester_int == 2:
        while True:
            course = nte_courses[randint(0, len(nte_courses) - 1)]
            if course not in total_course_list:
                if check_for_quota(course):
                    my_course_list.append(course)
                    total_course_list.append(course)
                    course.number_of_student += 1
                else:
                    error = "The system didnt allow NTE - " + course.course_name + " because quota is full!"
                    student.errors.append(error)

                    if student.student_number not in student.advisor.quota_error_list:
                        student.advisor.quota_error_list.append(student.student_number)
                break

    elif semester_int == 7:
        while True:
            course = te_courses[randint(0, len(te_courses) - 1)]
            if course not in total_course_list:
                if check_for_quota(course):
                    my_course_list.append(course)
                    total_course_list.append(course)
                    course.number_of_student += 1
                else:
                    error = "The system didnt allow TE - " + course.course_name + " because quota is full!"
                    student.errors.append(error)

                    if student.student_number not in student.advisor.quota_error_list:
                        student.advisor.quota_error_list.append(student.student_number)
                break

        while True:
            course = ue_courses[randint(0, len(ue_courses) - 1)]
            if course not in total_course_list:
                if check_for_quota(course):
                    my_course_list.append(course)
                    total_course_list.append(course)
                    course.number_of_student += 1
                else:
                    error = "The system didnt allow ENG - UE" + course.course_name + " because quota is full!"
                    student.errors.append(error)

                    if student.student_number not in student.advisor.quota_error_list:
                        student.advisor.quota_error_list.append(student.student_number)
                break

    elif semester_int == 8:
        for i in range(3):
            while True:
                course = te_courses[randint(0, len(te_courses) - 1)]
                if course not in total_course_list:
                    if check_for_quota(course):
                        my_course_list.append(course)
                        total_course_list.append(course)
                        course.number_of_student += 1
                    else:
                        error = "The system didnt allow TE - " + course.course_name + " because quota is full!"
                        student.errors.append(error)

                        if student.student_number not in student.advisor.quota_error_list:
                            student.advisor.quota_error_list.append(student.student_number)
                    break

        while True:
            course = fte_courses[randint(0, len(fte_courses) - 1)]
            if course not in total_course_list:
                if check_for_quota(course):
                    my_course_list.append(course)
                    total_course_list.append(course)
                    course.number_of_student += 1
                else:
                    error = "The system didnt allow ENG-FTE - " + course.course_name + " because quota is full!"
                    student.errors.append(error)

                    if student.student_number not in student.advisor.quota_error_list:
                        student.advisor.quota_error_list.append(student.student_number)
                break

        while True:
            course = nte_courses[randint(0, len(nte_courses) - 1)]
            if course not in total_course_list:
                if check_for_quota(course):
                    my_course_list.append(course)
                    total_course_list.append(course)
                    course.number_of_student += 1
                else:
                    error = "The system didnt allow NTE - " + course.course_name + " because quota is full!"
                    student.errors.append(error)

                    if student.student_number not in student.advisor.quota_error_list:
                        student.advisor.quota_error_list.append(student.student_number)
                break

    for i in range(0, len(my_course_list)):
        for j in range(i + 1, len(my_course_list)):
            for k in range(0, len(my_course_list[i].course_hour)):
                for n in range(0, len(my_course_list[j].course_hour)):
                    if my_course_list[i].course_hour[k] == my_course_list[j].course_hour[n]:
                        error = ("There is a collision between " + my_course_list[i].course_name + " " + str(
                            k + 1) + ".hour and " + my_course_list[j].course_name + " " + str(n + 1) + ".hour")
                        student.errors.append(error)
                        if student.student_number not in student.advisor.collision_error_list:
                            student.advisor.collision_error_list.append(student.student_number)
                            logging.warning(student.student_number + " - " + error)  # will print a message to the console

    return my_course_list


def check_for_quota(course):
    if course.number_of_student >= course.quota:
        return False
    else:
        return True


def semester_to_int(year):
    if semester == "FALL":
        return year * 2 - 1
    else:
        return year * 2


def get_numeric_grade_from_letter_grade(letter_grade):
    match letter_grade:
        case 'AA':
            return 4.0
        case 'BA':
            return 3.5
        case 'BB':
            return 3.0
        case 'CB':
            return 2.5
        case 'CC':
            return 2.0
        case 'DC':
            return 1.5
        case 'DD':
            return 1.0
        case 'FD':
            return 0.5
        case _:
            return 0.0


def generate_student_number(year, count):
    number_start = str(150122 - year)
    number_start += "0"

    if count >= 9:
        student_number = str(number_start) + str(count + 1)

    else:
        student_number = str(number_start) + str(count // 10) + str(count + 1)

    return student_number


def generate_random_name():
    first_names = ("Ahmet", "Mehmet", "Mustafa", "Zeynep", "Elif", "Defne", "Kerem", "Azra", "Miran",
                   "Asya", "Hamza", "Öykü", "Ömer Asaf", "Ebrar", "Ömer", "Eylül", "Eymen", "Murat", "Hesna", "Ali",
                   "Nuri",
                   "Muhammed", "Gökay", "Koray", "Esra", "Bihter", "Ceyda", "Özge", "Özlem", "Önder", "Ramazan",
                   "Recep",
                   "Rabia", "Hilal", "Buse", "Başak", "Serkan", "Ulaş", "Deniz", "Kardelen", "Mervan", "Kübra",
                   "Atilla",
                   "İlhan", "Fatih", "Asena", "Ahsen", "Ferit", "Kemal")

    last_names = ("Yılmaz", "Deniz", "Karakurt", "Şahin", "Türkay", "Akyıldız", "Yıldız", "Güçlü",
                  "Temur", "Duraner", "Yılmazer", "Ekşi", "Ballıca", "Erdoğmuş", "Erdoğan", "Korkmaz", "Çubukluöz",
                  "Hüyüktepe", "Zengin", "Büyük", "Küçük", "Türk", "Turgut", "Boz", "Açıkgöz", "Öztürk", "Beler",
                  "Çetin", "Bilgin", "Yalçınkaya", "Adıgüzel", "Kartal", "Dinç", "Genç", "Kuruçay", "Parlak",
                  "Karakaya",
                  "Kaya")

    full_name = first_names[randint(0, len(first_names) - 1)] + " " + last_names[randint(0, len(last_names) - 1)]

    return full_name


def generate_random_letter_grade():
    grades = ("AA", "BA", "BB", "BB", "CB", "CC", "DC", "DD", "FD", "FF")

    return grades[randint(0, len(grades) - 1)]


def create_json_for_all_students():
    for student in student_list:
        student.toJSON()


def add_approval_courses_for_all_student():
    for advisor in advisor_list:
        advisor.add_approval_courses()


def print_error_log():
    for advisor in advisor_list:
        if len(advisor.student_list) != 0:
            if len(advisor.quota_error_list) != 0:
                print(advisor.advisor_name + f"'s quota list ({len(advisor.quota_error_list)} students):")
                print(advisor.quota_error_list)
            if len(advisor.prerequisite_error_list) != 0:
                print(advisor.advisor_name + f"'s prerequisite list ({len(advisor.prerequisite_error_list)} students):")
                print(advisor.prerequisite_error_list)
            if len(advisor.collision_error_list) != 0:
                print(advisor.advisor_name + f"'s collison list ({len(advisor.collision_error_list)} students):")
                print(advisor.collision_error_list)
            if len(advisor.te_error_list) != 0:
                print(advisor.advisor_name + f"'s TE error list ({len(advisor.te_error_list)} students):")
                print(advisor.te_error_list)
            if len(advisor.project_error_list) != 0:
                print(advisor.advisor_name + f"'s Project Error list ({len(advisor.project_error_list)} students):")
                print(advisor.project_error_list)


if __name__ == '__main__':
    logging.basicConfig(filename='ErrorLog.log', encoding='utf-8', level=logging.DEBUG)

    student_list = []
    advisor_list = get_advisors_from_json()
    semester = get_semester_from_json()
    course_list = create_courses()

    initialize_students()
    add_approval_courses_for_all_student()
    print_error_log()

    if get_create_new_student_from_json():
        create_json_for_all_students()
