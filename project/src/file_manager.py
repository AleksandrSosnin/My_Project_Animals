import os

class FileManager:
    def __init__(self, pet_file, livestock_file, combined_file):
        self.pet_file = pet_file
        self.livestock_file = livestock_file
        self.combined_file = combined_file

    def create_files(self):
        # Создание файлов с животными
        pet_data = [
            "Барсик, Сидеть, 2020-01-15",
            "Мурка, Лежать, 2019-03-10",
            "Фишка, Крутить колесо, 2021-06-01"
        ]

        livestock_data = [
            "Лошадь, Тянуть плуг, 2018-05-20",
            "Верблюд, Переносить груз, 2017-11-30",
            "Осел, Носить вещи, 2016-02-17"
        ]

        os.makedirs(os.path.dirname(self.pet_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.livestock_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.combined_file), exist_ok=True)

        with open(self.pet_file, 'w', encoding='utf-8') as f:
            for item in pet_data:
                f.write(item + '\n')

        with open(self.livestock_file, 'w', encoding='utf-8') as f:
            for item in livestock_data:
                f.write(item + '\n')

        # Объединение файлов
        with open(self.combined_file, 'w', encoding='utf-8') as f:
            for item in pet_data + livestock_data:
                f.write(item + '\n')

        print("Файлы успешно созданы и заполнены.")
