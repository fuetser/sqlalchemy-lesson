from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import Table, orm
from db_session import SqlAlchemyBase


jobs_to_categories = Table(
    'association', SqlAlchemyBase.metadata,
    Column('jobs', Integer, ForeignKey('jobs.id')),
    Column('category', Integer, ForeignKey('category.id'))
)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String, default="password")
    modified_date = Column(DateTime, default=datetime.now)


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey("users.id"))
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    is_finished = Column(Boolean)
    categories = orm.relation(
        "Category", secondary="association", backref="jobs")


class Department(SqlAlchemyBase):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief = Column(Integer, ForeignKey("users.id"))
    members = Column(String)
    email = Column(String)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
