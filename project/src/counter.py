class Counter:
    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1
        print(f"Текущее значение счетчика: {self.count}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            print("Произошла ошибка во время работы с объектом 'Counter'.")
        else:
            print("Работа с объектом типа 'Counter' завершена без ошибок")
