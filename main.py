from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from Database import Base, engine, SessionLocal

class Student(Base):
    __tablename__ = "students"
    
    
    stuname = Column(String, index=True)
    stuage = Column(Integer)
    stuid = Column(Integer, primary_key=True, index=True)
    sturollno = Column(Integer, unique=True, index=True)
    stuadress = Column(String)

class StudentSchema(BaseModel):
    stuname: str
    stuage: int
    sturollno: int
    stuadress: str

class StudentRead(StudentSchema):
    stuid: int
    
    class Config:
        from_attributes = True 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/students/", response_model=StudentRead)
def create_student(student: StudentSchema, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[StudentRead])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

@app.get("/students/{student_id}", response_model=StudentRead)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.stuid == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student