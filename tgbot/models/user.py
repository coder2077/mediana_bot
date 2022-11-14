from sqlalchemy import Column, BigInteger, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


from tgbot.models import BaseModel, Base


association_table = Table(
	"students_subscribed",
	BaseModel.metadata, 
	Column("student_id", ForeignKey("students.user_id")),
	Column("course_id", ForeignKey("courses.id")),
)

class Register(Base):
	__tablename__ = 'students_subscribed'
	__table_args__ = {'extend_existing': True}

	student_id = Column(ForeignKey("students.user_id"), primary_key=True)
	course_id = Column(ForeignKey("courses.id"), primary_key=True)


class User(BaseModel):
	__tablename__ = 'students'

	user_id = Column(BigInteger(), nullable=False, autoincrement=False, primary_key=True)
	referral = Column(String(length=50), nullable=True, default=None)
	full_name = Column(String(length=255), nullable=False)
	phone = Column(String(length=300), default=None)
	username = Column(String(length=255), default=None)
	subscribed = relationship("Course", secondary=association_table)
	offline_study = Column(Boolean(), default=False, nullable=True)
	registered = Column(Boolean(), default=False, nullable=True)
	mediana = Column(Integer(), default=0)
	blocked = Column(Boolean(), default=False)
