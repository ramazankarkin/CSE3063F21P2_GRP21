# import required packages
import json
from random import randint
from Student import Student
from Advisor import Advisor
from Course import Course
from Transcript import Transcript

def get_create_new_student_from_json():
    json_file = open("input.json")
    variables = json.load(json_file)
    json_file.close()

    return True if variables['createNewStudents'] == True else False 

def get_semester_from_json():
    json_file = open("input.json")
    variables = json.load(json_file)
    json_file.close()

    return variables['semester']

def get_advisors_from_json():
    json_file = open("input.json")

    with open("input.json", encoding='utf-8') as data_file:
        data=json.load(data_file)

    variables = json.load(json_file)
    json_file.close()

    advisor_list = []

    for advisor in variables['advisors']:
        new_advisor = Advisor(advisor['advisorName'], advisor['department'], advisor['rank'])
        advisor_list.append(new_advisor)
        
    return advisor_list

def create_courses():
    course_list = []

    for semester in range(1, 9):
        course_list += create_semester_courses(semester)

    course_list += create_elective_courses("NTE")
    course_list += create_elective_courses("ENG-UE")
    course_list += create_elective_courses("TE")
    course_list += create_elective_courses("ENG-FTE")

    return course_list

def create_semester_courses(semester):
    json_file = open("input.json")
    variables = json.load(json_file)
    json_file.close()

    myCourseList = []
    
    for courses in variables['courses']:
        for semester_course in courses[str(semester)]:
            new_course = Course(semester_course['courseName'], semester_course['courseCredit'],
            semester, None, None, None, semester_course['courseHourCode'])
            
            if 'prerequisite' in semester_course:
                new_course.prerequisite = semester_course['prerequisite']
            
            myCourseList.append(new_course)

    return myCourseList

def create_elective_courses(electiveType):
    json_file = open("input.json")
    variables = json.load(json_file)
    json_file.close()

    myCourseList = []
    
    for courses in variables['courses']:
        for semester in courses[electiveType]:
            new_course = Course(semester['courseName'], semester['courseCredit'],
            None, semester['quota'], None, electiveType, semester['courseHourCode'])

            if 'prerequisite' in semester:
                new_course.prerequisite = semester['prerequisite']

            myCourseList.append(new_course)

    return myCourseList

def get_semester_courses(semester):
    my_course_list = []

    for course in course_list:
        if(course.semester == semester):
            my_course_list.append(course)

    return my_course_list

def get_elective_courses(elective_type):
    my_course_list = []

    for course in course_list:
        if(course.elective_type == elective_type):
            my_course_list.append(course)

    return my_course_list

def initialize_students():
    for year in range(1,5):
        advisor = advisor_list[randint(0, len(advisor_list)-1)]
        for y in range(70):
            student = Student(generate_student_number(year,y), generate_random_name(), year, advisor, create_transcript(year),
            None, None)
            student.course_offerd = create_course_offered(student)
            student_list.append(student)

def create_transcript(year):
    my_course_list = []
    point = 0
    given_credit = 0
    completed_credit = 0
    gano = 0

    for semester in range(1, semester_to_int(year)):
        for course in get_semester_courses(semester):
            letter_grade = generate_random_letter_grade()
            my_course_list.append({"course" : course, "letterGrade" : letter_grade})
        
        
        # if(semester == 2):
        #     while(True):
        #         electiveCourse = get_elective_courses("NTE")[randint(0, len(get_elective_courses("NTE"))-1)]
        #         if my_course_list.count(electiveCourse) == 0:
        #             my_course_list.append({"course" : electiveCourse, "letterGrade" : generateRandomLetterGrade(), "semester" : semester})
        #             break

    transcript = Transcript(my_course_list, given_credit, completed_credit, point, gano)
    return transcript

def create_course_offered(student):
    error_list = []
    my_course_list = []

    semester_int = semester_to_int(student.year)

    semester_courses = get_semester_courses(semester_int)
    
    for course in semester_courses:
        my_course_list.append(course)

    nte_courses = get_elective_courses("NTE")
    te_courses = get_elective_courses("TE")
    ue_courses = get_elective_courses("ENG-UE")
    fte_courses = get_elective_courses("ENG-FTE")

    if semester_int == 2:
        while(True):
            course = nte_courses[randint(0, len(nte_courses)-1)]
            if course not in student.transcript_before.course_list:
                if(check_for_quota(course) == True):
                    my_course_list.append(course)
                    break
                else:
                    error = "The system didnt allow " + course.course_name + " because quota is full!"
                    error_list.append(error)

    return my_course_list

def check_for_quota(course):
    if(len(course.student_list) >= course.quota):
        return False
    else:
        return True

def semester_to_int(year):
    if(semester == "FALL"):
        return year*2-1
    else:
        return year*2

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
    
    if count>=9:
        student_number = str(number_start) + str(count+1)

    else:
        student_number = str(number_start) + str(count//10) + str(count+1)

    return student_number

def generate_random_name():
    first_names = ("Ahmet", "Mehmet", "Mustafa", "Zeynep", "Elif", "Defne", "Kerem", "Azra", "Miran",
                "Asya", "Hamza", "Öykü", "Ömer Asaf", "Ebrar", "Ömer", "Eylül", "Eymen", "Murat", "Hesna", "Ali", "Nuri",
                "Muhammed", "Gökay", "Koray", "Esra", "Bihter", "Ceyda", "Özge", "Özlem", "Önder", "Ramazan", "Recep",
                "Rabia", "Hilal", "Buse", "Başak", "Serkan", "Ulaş", "Deniz", "Kardelen", "Mervan", "Kübra", "Atilla",
                "İlhan", "Fatih", "Asena", "Ahsen", "Ferit", "Kemal")

    last_names = ("Yılmaz", "Deniz", "Karakurt", "Şahin", "Türkay", "Akyıldız", "Yıldız", "Güçlü",
                "Temur", "Duraner", "Yılmazer", "Ekşi", "Ballıca", "Erdoğmuş", "Erdoğan", "Korkmaz", "Çubukluöz",
                "Hüyüktepe", "Zengin", "Büyük", "Küçük", "Türk", "Turgut", "Boz", "Açıkgöz", "Öztürk", "Beler",
                "Çetin", "Bilgin", "Yalçınkaya", "Adıgüzel", "Kartal", "Dinç", "Genç", "Kuruçay", "Parlak", "Karakaya",
                "Kaya")

    full_name = first_names[randint(0, len(first_names)-1)] + " " + last_names[randint(0, len(last_names)-1)]

    return full_name

def generate_random_letter_grade():
    grades = ("AA", "BA", "BB", "BB", "CB", "CC", "DC", "DD", "FD", "FF")

    return grades[randint(0, len(grades)-1)]

def create_json_for_all_students():
    for student in student_list:
        student.toJSON()

if __name__ == '__main__':
    student_list = []
    advisor_list = get_advisors_from_json()
    semester = get_semester_from_json()
    course_list = create_courses()

    initialize_students()
    create_json_for_all_students()