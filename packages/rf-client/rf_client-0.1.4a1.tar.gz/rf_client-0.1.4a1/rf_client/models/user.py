class User:
    """
    Модель для пользователя карты
    """

    def __init__(self, id, username, name, surname, avatar, is_admin, can_export):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.avatar = avatar
        self.is_admin = is_admin
        self.can_export = can_export

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', " \
               f"'{self.name}', '{self.surname}', '{self.avatar}', '{self.is_admin}', '{self.can_export}')"
