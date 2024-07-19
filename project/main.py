from src.file_manager import FileManager
from src.database_manager import DatabaseManager
from src.animal_registry import Pet, Livestock
from src.counter import Counter

def main():
    host = 'localhost'
    user = 'root'
    password = '1111'
    database = 'FriendsOfHumans'

    db_manager = DatabaseManager(host, user, password, database)
    db_manager.connect()
    
    db_manager.create_database()
    db_manager.create_tables()
    
    # Заполнение таблиц
    db_manager.insert_domestic_animal("Dog", "Sit", "2019-01-10")
    db_manager.insert_domestic_animal("Cat", "Meow", "2020-05-15")
    db_manager.insert_domestic_animal("Hamster", "Run in wheel", "2020-08-20")
    
    db_manager.insert_livestock_animal("Horse", "Pull plow", "2018-03-25")
    db_manager.insert_livestock_animal("Camel", "Carry load", "2017-06-10")
    db_manager.insert_livestock_animal("Donkey", "Carry items", "2019-09-05")
    
    # Удаление верблюда
    db_manager.delete_livestock_animal("Camel")
    
    # Объединение лошадей и ослов
    db_manager.merge_horses_donkeys()
    
    # Создание и заполнение таблицы молодых животных
    db_manager.create_young_animals_table()
    db_manager.populate_young_animals()
    
    # Объединение всех таблиц
    db_manager.merge_all_animals()
    
    db_manager.close_connection()

if __name__ == "__main__":
    main()
