import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    town = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    register_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    requestsam = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.town} {self.register_date}'
