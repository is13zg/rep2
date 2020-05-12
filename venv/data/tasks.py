import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ans1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ans2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ans3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ans4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tests = orm.relation('Tests')