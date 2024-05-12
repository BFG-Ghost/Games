import redis
import json


class PhoneBook:
    def __init__(self):
        self.red = redis.Redis(host='127.0.0.1')
        self.process()

    def get_contact(self, name):
        try:
            return json.loads(self.red.get(name))
        except Exception:
            return None

    def add_contact(self, name, phone):
        self.red.set(name, phone)

    def delete_contact(self, name):
        self.red.delete(name)

    def process(self):
        help = """
        get <name> - получить данные контакта
        add <name> <phone> - добавить контакт с номером
        del <name> - удалить контакт с именем
        """
        print(help)
        while True:
            cmd = input('->')
            command = cmd.split(' ')[0].lower()
            if command == 'get':
                _, name = cmd.split(' ')
                print(f'{str(self.get_contact(name))}')
            elif command == 'add':
                _, name, phone = cmd.split(' ')
                if self.get_contact(name) is None:
                    self.add_contact(name, phone)
                    print(f'Контакт {name} добавлен')
                else:
                    print('Контакт с таким именем уже существует')
            elif command == 'del':
                _, name = cmd.split(' ')
                self.delete_contact(name)
                print(f'Контакт {name} удалён')
            elif command == 'help':
                print(help)
            elif command == 'q':
                exit(0)
            else:
                print('Команда не распознана')


if __name__ == "__main__":
    pb = PhoneBook()
