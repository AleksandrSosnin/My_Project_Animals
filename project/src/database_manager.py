import mysql.connector

class DatabaseManager:
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

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"База данных '{self.database}' успешно создана или уже существует.")
        except mysql.connector.Error as e:
            print(f"Ошибка при создании базы данных: {e}")

    def create_tables(self):
        create_domestic_animals_table = """
        CREATE TABLE IF NOT EXISTS domestic_animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            command VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL
        );
        """
        create_livestock_animals_table = """
        CREATE TABLE IF NOT EXISTS livestock_animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            command VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL
        );
        """
        try:
            self.cursor.execute(create_domestic_animals_table)
            self.cursor.execute(create_livestock_animals_table)
            self.conn.commit()
            print("Таблицы 'domestic_animals' и 'livestock_animals' успешно созданы или уже существуют.")
        except mysql.connector.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

    def insert_domestic_animal(self, name, command, birth_date):
        insert_query = """
        INSERT INTO domestic_animals (name, type, command, birth_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (name, "Domestic", command, birth_date)
        
        try:
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print(f"Домашнее животное '{name}' успешно добавлено в таблицу 'domestic_animals'.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении домашнего животного '{name}': {e}")

    def insert_livestock_animal(self, name, animal_type, birth_date):
        insert_query = """
        INSERT INTO livestock_animals (name, type, command, birth_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (name, "Livestock", animal_type, birth_date)
        
        try:
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print(f"Вьючное животное '{name}' успешно добавлено в таблицу 'livestock_animals'.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении вьючного животного '{name}': {e}")

    def delete_livestock_animal(self, name):
        delete_query = """
        DELETE FROM livestock_animals
        WHERE name = %s
        """
        try:
            self.cursor.execute(delete_query, (name,))
            self.conn.commit()
            print(f"Вьючное животное '{name}' успешно удалено из таблицы 'livestock_animals'.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при удалении вьючного животного '{name}': {e}")

    def merge_horses_donkeys(self):
        merge_query = """
        INSERT INTO livestock_animals (name, type, command, birth_date)
        SELECT name, 'HorseOrDonkey' AS type, command, birth_date
        FROM horses
        UNION
        SELECT name, 'HorseOrDonkey' AS type, command, birth_date
        FROM donkeys
        """
        try:
            self.cursor.execute(merge_query)
            self.conn.commit()
            print("Таблицы 'horses' и 'donkeys' успешно объединены в таблицу 'livestock_animals'.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при объединении таблиц 'horses' и 'donkeys': {e}")

    def create_young_animals_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS young_animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            animal_type VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            age_months INT NOT NULL
        )
        """
        try:
            self.cursor.execute(create_query)
            self.conn.commit()
            print("Таблица 'young_animals' успешно создана или уже существует.")
        except mysql.connector.Error as e:
            print(f"Ошибка при создании таблицы 'young_animals': {e}")

    def populate_young_animals(self):
        populate_query = """
        INSERT INTO young_animals (name, animal_type, birth_date, age_months)
        SELECT name, animal_type, birth_date,
        TIMESTAMPDIFF(MONTH, birth_date, CURDATE()) AS age_months
        FROM livestock_animals
        WHERE TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) BETWEEN 1 AND 3
        """
        try:
            self.cursor.execute(populate_query)
            self.conn.commit()
            print("Таблица 'young_animals' успешно заполнена.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при заполнении таблицы 'young_animals': {e}")

    def merge_all_animals(self):
        merge_query = """
        CREATE TABLE IF NOT EXISTS all_animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            animal_type VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            original_table VARCHAR(255) NOT NULL
        )
        """
        insert_query = """
        INSERT INTO all_animals (name, animal_type, birth_date, original_table)
        SELECT name, 'Domestic' AS animal_type, birth_date, 'domestic_animals' AS original_table
        FROM domestic_animals
        UNION
        SELECT name, 'Livestock' AS animal_type, birth_date, 'livestock_animals' AS original_table
        FROM livestock_animals
        """
        try:
            self.cursor.execute(merge_query)
            self.cursor.execute(insert_query)
            self.conn.commit()
            print("Таблицы 'domestic_animals' и 'livestock_animals' успешно объединены в таблицу 'all_animals'.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Ошибка при объединении таблиц 'domestic_animals' и 'livestock_animals': {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Отключение от базы данных выполнено.")
