"""
У користувача буде адресна книга або книга контактів. 
Ця книга контактів містить записи. 
Кожен запис містить деякий набір полів.

Користувач взаємодіє з книгой контактів, додаючи, видаляючи та редагуючи записи. 
Також користувач повинен мати можливість шукати в книзі контактів записи за одному або декількома критеріями (полям).

Поля можуть бути обов'язковими (ім'я) та необов'язковими (телефон або email наприклад).
Також записи можуть містити декілька полів одного типу (декілька телефонів наприклад). 
Користувач повинен мати можливість додавати/видаляти/редагувати поля у будь-якому записі.

В цій домашній роботі ви повинні реалізувати такі класи:

Клас AddressBook, який успадковується від UserDict, та ми потім додамо логіку пошуку за записами до цього класу.
Клас Field, який буде батьківським для всіх полів, у ньому потім реалізуємо логіку загальну для всіх полів.
Клас Name, обов'язкове поле з ім'ям.
Клас Phone, необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.
Клас Record, який відповідає за логіку додавання/видалення/редагування необов'язкових полів 
   та зберігання обов'язкового поля Name.

Критерії прийому:
Реалізовано всі класи із завдання.
Записи Record у AddressBook зберігаються як значення у словнику. 
В якості ключів використовується значення Record.name.value.
Record зберігає об'єкт Name в окремому атрибуті.
Record зберігає список об'єктів Phone в окремому атрибуті.
Record реалізує методи для додавання/видалення/редагування об'єктів Phone.
AddressBook реалізує метод add_record, який додає Record у self.data.
"""

from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def is_valid_phone(self):
        pass        

class Email(Field):
    def is_valid_email(self):
        pass        

class Record:
    def __init__(self, name: str, phones: list, emails: list):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.emails = [Email(email) for email in emails]

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None        

    def delete_phone(self, value):
        phone_to_delete = self.find_phone(value)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def add_email(self, email):
        email_addr = Email(email)
        if email_addr not in self.emails:
            self.emails.append(email_addr)

    def find_email(self, value):
        for email in self.emails:
            if email.value == value:
                return email
        return None        

    def delete_email(self, value):
        email_to_delete = self.find_email(value)
        if email_to_delete:
            self.pemails.remove(email_to_delete)

    def edit_email(self, old_email, new_email):
        email_to_edit = self.find_email(old_email)
        if email_to_edit:
            email_to_edit.value = new_email

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)    

def add_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    email = data[2]
    record = address_book.find_record(name)
    if record:
        if phone: 
            record.add_phone(phone)
            return f"Phone {phone} was added to contact {name}"
        if email:
            record.add_email(email)
            return f"Email {email} was added to contact {name}"            
    else:
        record = Record(name, [phone], [email])
        address_book.add_record(record)
        return f"Contact {name} with phone {phone} and email {email} was saved"

def change_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    email = data[2]
    record = address_book.find_record(name)
    if record:
        if phone: 
            record.edit_phone(phone, phone)
            return f"Phone number for contact {name} was changed to {phone}"
        if email: 
            record.edit_email(email, email)
            return f"Email number for contact {name} was changed to {email}"
    else:
        return "Contact not found"

def phone_handler(address_book, data):
    name = data[0].title()
    record = address_book.find_record(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        emails = ", ".join([email.value for email in record.emails])
        return f"{name} has phones: {phones} and emails {emails}"
    else:
        return "Contact not found"

def show_all_handler(address_book, *args):
    if not address_book.data:
        return "The address book is empty"
    for name, record in address_book.data.items():
        contacts = "\n".join([f"{name}: "                                            + \
                                {' '.join([phone.value for phone in record.phones])} + \
                                {' '.join([email.value for email in record.emails])} + \
                            " "])
    return contacts

def hello_handler(address_book, *args):
    return "How can I help you?"

def exit_handler(address_book, *args):
    return "Good bye!"

def command_parser(raw_str: str):  # Парсер команд
    elements = raw_str.split()
    for func, cmd_list in COMMANDS.items():
        for cmd in cmd_list:
            if elements[0].lower() == cmd:
                return func, elements[1:]
    return None, None

COMMANDS = {
    add_handler: ["add"],
    change_handler: ["change"],
    phone_handler: ["phone"],
    show_all_handler: ["show all"],
    exit_handler: ["good bye", "close", "exit"],
    hello_handler: ["hello"]
}

def main():
    address_book = AddressBook()

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)
        if not func:
            print("Unknown command. Type 'hello' for available commands.")
        else:
            result = func(address_book, data)
            print(result)
            if func == exit_handler:
                break

if __name__ == "__main__":
    main()
