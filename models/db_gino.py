import logging
from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    discord_id = db.Column(db.Integer())
    user_name = db.Column(db.Unicode())
    birth_date = db.Column(db.Date())

    @property
    def month_and_day(self):
        return self.birth_date.strftime(format="%d.%m")

    def __str__(self):
        return self.user_name


async def on_startup(url):
    logging.info("set bind to PostgreSQL")
    await db.set_bind(url)
    logging.info("prepare tables PostgreSQL")
    await db.gino.create_all()
