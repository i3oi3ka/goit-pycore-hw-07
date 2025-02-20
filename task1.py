"""  Usage Example"""

from task_1.address_book import AddressBook
from task_1.record import Record

if __name__ == "__main__":

    # Create a new address book
    book = AddressBook()

    # Create a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Add John's record to the address book
    book.add_record(john_record)

    # Create and add a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Print all records in the book
    for name, record in book.data.items():
        print(record)

    # Find and edit a phone number for John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john.add_birthday("01.10.1989")

    print(john)
    print(john.birthday)  # Output: Contact name: John, phones: 1112223333; 5555555555
    john.edit_phone("5555555555", "1112223333")
    print(john)
    # Find a specific phone number in John's record
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Output: 5555555555

    # Delete Jane's record
    book.delete("Jane")

    vova = Record("Vova")
    vova.add_birthday("02.08.1989")
    book.add_record(vova)
    book.add_record(Record("Vasya"))

    print(book.get_upcoming_birthdays())
