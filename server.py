from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.model import Base
from config.config import PostgresDB
from views import views

class MainApp(PostgresDB):
    def __init__(self, host, database, user, password, port=5432):
        super().__init__(host, database, user, password, port)
        self.DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def run(self):
        # Connect raw psycopg2
        self.connect()
        Base.metadata.create_all(self.engine)
        print("ORM tables ready")

        session = self.SessionLocal()

        while True:
            print("\n===== MENU =====")
            print("1. Add Student")
            print("2. Add Course")
            print("3. Enroll Student")
            print("4. List Students & Courses")
            print("5. Show Top Students (>75)")
            print("6. Show Courses Without Students")
            print("7. Update Marks")
            print("8. Delete Course")
            print("9. Transaction Demo")
            print("0. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                views.add_student(session, input("Name: "), input("Program: "))
            elif choice == "2":
                views.add_course(session, input("Course Name: "), int(input("Credits: ")))
            elif choice == "3":
                views.enroll_student(session, int(input("Student ID: ")), int(input("Course ID: ")), float(input("Marks: ")))
            elif choice == "4":
                views.list_students(session)
            elif choice == "5":
                views.top_students(session)
            elif choice == "6":
                views.courses_without_students(session)
            elif choice == "7":
                views.update_marks(session, int(input("Enrollment ID: ")), float(input("New Marks: ")))
            elif choice == "8":
                views.delete_course(session, int(input("Course ID: ")))
            elif choice == "9":
                views.transaction_demo(session)
            elif choice == "0":
                break
            else:
                print("Invalid choice")

        session.close()
        self.close()

if __name__ == "__main__":
    app = MainApp(
        host="localhost",
        database="student_course_db",
        user="postgres",
        password="root",
        port=5432
    )
    app.run()
