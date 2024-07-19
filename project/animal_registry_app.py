
import mysql.connector
from mysql.connector import errorcode

class AnimalRegistryApp:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(buffered=True)
            print("Подключение к базе данных успешно.")
        except mysql.connector.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Отключение от базы данных выполнено.")

    def add_animal(self, name, animal_type, command, birth_date):
        insert_query = """
        INSERT INTO animals (name, type, command, birth_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (name, animal_type, command, birth_date)
        
        try:
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print(f"Животное '{name}' успешно добавлено в реестр.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении животного '{name}' в реестр: {e}")

    def delete_animal(self, name):
        delete_query = """
        DELETE FROM animals
        WHERE name = %s
        """
        data = (name,)
        
        try:
            self.cursor.execute(delete_query, data)
            self.conn.commit()
            print(f"Животное '{name}' успешно удалено из реестра.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при удалении животного '{name}' из реестра: {e}")

    def view_animals(self):
        select_query = """
        SELECT name, type, command, birth_date FROM animals
        """
        
        try:
            self.cursor.execute(select_query)
            animals = self.cursor.fetchall()
            if animals:
                print("Список зарегистрированных животных:")
                for animal in animals:
                    print(f"Имя: {animal[0]}, Тип: {animal[1]}, Команда: {animal[2]}, Дата рождения: {animal[3]}")
            else:
                print("Реестр животных пуст.")
        except mysql.connector.Error as e:
            print(f"Ошибка при просмотре списка животных: {e}")

if __name__ == "__main__":
    # Параметры подключения к базе данных
    host = 'localhost'
    user = 'root'
    password = '1111'
    database = 'FriendsOfHumans'

    app = AnimalRegistryApp(host, user, password, database)
    app.connect()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить животное")
        print("2. Удалить животное")
        print("3. Просмотреть список животных")
        print("4. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == '1':
            name = input("Введите имя животного: ")
            animal_type = input("Введите тип животного (домашнее/вьючное): ")
            command = input("Введите команду или действие: ")
            birth_date = input("Введите дату рождения (гггг-мм-дд): ")
            app.add_animal(name, animal_type, command, birth_date)
        
        elif choice == '2':
            name = input("Введите имя животного для удаления: ")
            app.delete_animal(name)
        
        elif choice == '3':
            app.view_animals()
        
        elif choice == '4':
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, выберите номер действия от 1 до 4.")

    app.disconnect()
