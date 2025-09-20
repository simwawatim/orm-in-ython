from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    program = Column(String(100))
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100))
    credits = Column(Integer)
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    marks = Column(Float)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
