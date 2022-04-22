import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class WeatherNotifications(SqlAlchemyBase):
    __tablename__ = 'weather_notifications'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    period = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hours_remain = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ntype = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_enable = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return f'<WeatherNotifications> {self.id} {self.user_id} {self.hours_remain} {self.ntype} {self.is_enable}'
