from forms.weather import WeatherNotifications


async def get_user_notifications(message_user_id: int, session):
    if session.query(WeatherNotifications).filter(message_user_id == WeatherNotifications.user_id).first() is None:
        user_notifications = WeatherNotifications()
        user_notifications.user_id = message_user_id
        user_notifications.is_enable = False
        session.add(user_notifications)
        session.commit()
    else:
        user_notifications = session.query(WeatherNotifications).filter(message_user_id == WeatherNotifications.user_id).first()
    return user_notifications
