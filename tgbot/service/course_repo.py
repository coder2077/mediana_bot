from sqlalchemy import insert, select, update, func

from tgbot.models.course import Course
from tgbot.models.user import Register
from tgbot.service.base_repo import BaseSQLAlchemyRepo


class CourseRepo(BaseSQLAlchemyRepo):
	model = Course

	async def get_course(self, name: str):
		sql = select(self.model).where(self.model.name == name)
		request = await self._session.execute(sql)
		course = request.scalar()
		return course

	async def add_user_to_course(self, user_id: int, course_id: str):
		sql_select = select(Register).where(Register.student_id == user_id, Register.course_id == course_id)
		request = await self._session.execute(sql_select)
		existed = request.scalar()
		if existed is None:
			try:
				sql = insert(Register).values(student_id=user_id, course_id=int(course_id))
				await self._session.execute(sql)
				await self._session.commit()
				return
			except Exception as e:
				print(e)
			return None
		else:
			return existed
