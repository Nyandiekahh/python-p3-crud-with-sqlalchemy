#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class
Base = declarative_base()

# Define the Student class
class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id_pk'),
        UniqueConstraint('email', name='unique_email'),
        CheckConstraint('grade BETWEEN 1 AND 12', name='grade_between_1_and_12')
    )
    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: {self.name}, Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create new student records
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(year=1879, month=3, day=14)
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(year=1912, month=6, day=23)
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # Reading records
    students = session.query(Student).all()
    print("All students:", students)

    students_by_name = session.query(Student).order_by(Student.name).all()
    print("Students ordered by name:", students_by_name)

    students_by_grade_desc = session.query(Student).order_by(desc(Student.grade)).all()
    print("Students ordered by grade (descending):", students_by_grade_desc)

    oldest_student = session.query(Student).order_by(desc(Student.birthday)).first()
    print("Oldest student:", oldest_student)

    # Updating records
    for student in session.query(Student):
        student.grade += 1
    session.commit()
    updated_students = session.query(Student).all()
    print("Updated students:", updated_students)

    # Deleting records
    query = session.query(Student).filter(Student.name == "Albert Einstein")
    albert_einstein = query.first()
    session.delete(albert_einstein)
    session.commit()
    deleted_student = query.first()
    print("Deleted student:", deleted_student)
    remaining_students = session.query(Student).all()
    print("Remaining students after deletion:", remaining_students)
