from conductor_bot.config import User


class UserInDb:
    def __init__(self, database: dict[str, User] = None):
        if database is None:
            database = {}
        self.__db: dict[str, User] = database

    async def delete_user(self, username: str):
        try:
            self.__db.pop(username)
        except:
            ...
            
    async def add_user(self, username: str, chat_id: str, id: str):
        self.__db[username] = User(username, chat_id, id)

    async def get_user_by_username(self, username: str) -> User:
        return self.__db[username]

    async def get_friend(self, username: str) -> User:
        for user in self.__db:
            if username != user:
                return self.__db[user]

    async def check_users(self, username: str):
        for user in self.__db:
            if username != user:
                return True
        return False


bd_users = UserInDb()