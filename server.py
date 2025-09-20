from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.model import Base
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.config import PostgresDB
import views

class MainApp(PostgresDB):
    def __init__(self, host, database, user, password, port=5432):
        super().__init__(host, database, user, password, port)
        self.DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def run(self):
        # Connect raw psycopg2
        self.connect()

        # Create tables
        Base.metadata.create_all(self.engine)
        print("✅ ORM tables created")

        # Run ORM operations
        session = self.SessionLocal()
        try:
            views.add_sample_data(session)
            views.query_students(session)
        except Exception as e:
            session.rollback()
            print("❌ ORM operation failed:", e)
        finally:
            session.close()

        # Close raw connection
        self.close()

if __name__ == "__main__":
    app = MainApp(
        host="localhost",
        database="student_course_db",
        user="postgres",
        password="root",  # your password
        port=5432
    )
    app.run()
