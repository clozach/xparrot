"""Database configuration and models for xParrot."""
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_NAME = os.getenv('MYSQL_DATABASE', 'xparrot')

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association tables for many-to-many relationships
task_projects = Table(
    'task_projects',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)

task_subprojects = Table(
    'task_subprojects',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('subproject_id', Integer, ForeignKey('subprojects.id'))
)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    notes = Column(String(1000))
    status = Column(String(50), default='')
    link = Column(String(255))
    created_time = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", secondary=task_projects, back_populates="tasks")
    subprojects = relationship("Subproject", secondary=task_subprojects, back_populates="tasks")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    
    tasks = relationship("Task", secondary=task_projects, back_populates="projects")

class Subproject(Base):
    __tablename__ = 'subprojects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    tasks = relationship("Task", secondary=task_subprojects, back_populates="subprojects")
    project = relationship("Project")

def init_db():
    """Initialize the database, creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
