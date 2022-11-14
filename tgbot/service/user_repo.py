from sqlalchemy import insert, select, update, func

from tgbot.models.user import User
from tgbot.service.base_repo import BaseSQLAlchemyRepo


class UserRepo(BaseSQLAlchemyRepo):
	model = User

	async def add_user(self, user_id: int, full_name: str, username: str, referral: str, phone: str = None, registered: bool = False):
		sql = insert(self.model).values(
			user_id=user_id,
			full_name=full_name,
			username=username,
			referral=referral, 
			phone=phone, 
			registered=registered
		)
		try:
			await self._session.execute(sql)
		except Exception as e:
			print(e)
			await self._session.rollback()
		await self._session.commit()

	async def get_user(self, user_id: int) -> model:
		sql = select(self.model).where(self.model.user_id == user_id)
		request = await self._session.execute(sql)
		user = request.scalar()
		return user

	async def get_users(self) -> model:
		sql = select(self.model)
		request = await self._session.execute(sql)
		user = request.scalars().all()
		return user

	async def get_offline_users(self) -> model:
		sql = select(self.model).filter(self.model.offline_study == True)
		request = await self._session.execute(sql)
		user = request.scalars().all()
		return user

	async def update_user(self, user_id: int, data: dict):
		sql = update(self.model).where(self.model.user_id == user_id).values(data)
		try:
			await self._session.execute(sql)
		except:
			await self._session.rollback()
		await self._session.commit()

	async def count_user(self):
		sql = select(func.count()).select_from(self.model)
		request = await self._session.execute(sql)
		return request.scalar()
