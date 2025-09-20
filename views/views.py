from model.model import Student, Course, Enrollment

# CREATE
def add_student(session, name, program):
    student = Student(name=name, program=program)
    session.add(student)
    session.commit()
    print(f"Student added: {name}")

def add_course(session, course_name, credits):
    course = Course(course_name=course_name, credits=credits)
    session.add(course)
    session.commit()
    print(f"Course added: {course_name}")

def enroll_student(session, student_id, course_id, marks):
    enrollment = Enrollment(student_id=student_id, course_id=course_id, marks=marks)
    session.add(enrollment)
    session.commit()
    print(f"Student {student_id} enrolled in course {course_id} with marks {marks}")

# READ
def list_students(session):
    students = session.query(Student).all()
    for s in students:
        print(f"{s.name} ({s.program})")
        for e in s.enrollments:
            print(f"{e.course.course_name} - Marks: {e.marks}")

def top_students(session):
    results = session.query(Student).join(Enrollment).filter(Enrollment.marks > 75).all()
    print("Students with marks > 75:")
    for s in results:
        print(f"{s.name}")

def courses_without_students(session):
    results = session.query(Course).filter(~Course.enrollments.any()).all()
    print("Courses with no students:")
    for c in results:
        print(f"   {c.course_name}")

# UPDATE
def update_marks(session, enrollment_id, new_marks):
    enrollment = session.query(Enrollment).get(enrollment_id)
    if enrollment:
        enrollment.marks = new_marks
        session.commit()
        print(f"Updated marks for enrollment {enrollment_id} → {new_marks}")
    else:
        print("Enrollment not found")

# DELETE
def delete_course(session, course_id):
    course = session.query(Course).get(course_id)
    if course and not course.enrollments:
        session.delete(course)
        session.commit()
        print(f"Deleted course {course.course_name}")
    else:
        print("Course not found or has enrollments")

# TRANSACTION DEMO
def transaction_demo(session):
    try:
        s1 = Student(name="Temp1", program="RollbackTest")
        s2 = Student(name="Temp2", program="RollbackTest")
        session.add_all([s1, s2])
        session.flush()
        raise Exception("Intentional error to trigger rollback")
        session.commit()
    except Exception as e:
        session.rollback()
        print("Transaction rolled back:", e)
