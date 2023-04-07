class User:
    def __init__(self, user_id, balance, notice):
        self.id = user_id
        self.balance = balance
        self.notice = notice

    @staticmethod
    def from_db_to_user(data: list):
        return User(
            user_id=data[0],
            balance=data[1],
            notice=data[2]
        )
