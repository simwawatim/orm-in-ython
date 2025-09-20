from model.model import Student, Course, Enrollment

def add_sample_data(session):
    # Insert students and courses
    s1 = Student(name="Alice", program="BIT")
    s2 = Student(name="Bob", program="CS")
    c1 = Course(course_name="Databases", credits=3)
    c2 = Course(course_name="Algorithms", credits=4)
    session.add_all([s1, s2, c1, c2])
    session.commit()

    # Enroll students
    e1 = Enrollment(student=s1, course=c1, marks=85)
    e2 = Enrollment(student=s2, course=c2, marks=78)
    session.add_all([e1, e2])
    session.commit()

def query_students(session):
    students = session.query(Student).all()
    for s in students:
        print(f"Student: {s.name}, Program: {s.program}")
        for e in s.enrollments:
            print(f"   Course: {e.course.course_name}, Marks: {e.marks}")
