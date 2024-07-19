class Animal:
    def __init__(self, name, command, birth_date):
        self.name = name
        self.command = command
        self.birth_date = birth_date

    def show_info(self):
        print(f"Имя: {self.name}, Команда: {self.command}, Дата рождения: {self.birth_date}")

class Pet(Animal):
    pass

class Livestock(Animal):
    pass

class Dog(Pet):
    pass

class Cat(Pet):
    pass

class Hamster(Pet):
    pass

class Horse(Livestock):
    pass

class Camel(Livestock):
    pass

class Donkey(Livestock):
    pass
