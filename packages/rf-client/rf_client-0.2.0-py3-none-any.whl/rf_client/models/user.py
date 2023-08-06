class User:
    """
    Модель для пользователя карты
    """
    def __init__(self, id, username, name, surname, is_admin):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.is_admin = is_admin

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"