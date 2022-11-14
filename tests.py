from sqlalchemy import Column, ForeignKey, Integer, create_engine, insert, String, select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship

from tgbot.models.user import User, Register
from tgbot.models.course import Course
from tgbot.config import make_db_uri

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/mediana", echo=True, future=True)
Session = sessionmaker(bind=engine)
session = Session()


# sql = select(User).where(User.user_id == 5401906481)
# request = session.execute(sql)
# user = request.scalar()
# for course in user.subscribed:
#     print(course.name)

# sql = select(Register)
# request = session.execute(sql)
# course = request.scalars().all()
# print(course[0].course_id)

