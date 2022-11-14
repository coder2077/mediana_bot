from sqlalchemy import Column, String, Integer

from tgbot.models import BaseModel


class Course(BaseModel):
    __tablename__ = 'courses'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(length=250), nullable=False)
