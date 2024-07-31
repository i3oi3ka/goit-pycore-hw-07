"""homework"""
import re
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """
    Base class for storing field values of a record.

    Attributes:
        value (str): The value of the field.
    """

    def __init__(self, value: str):
        """
        Initializes the field.

        Args:
            value (str): The value of the field.
        """
        self.value = value

    def __str__(self) -> str:
        """
        Returns a string representation of the field value.

        Returns:
            str: The value of the field as a string.
        """
        return str(self.value)


class Name(Field):
    """
    Class for storing a contact's name. Inherits from Field.
    """
    pass


class Phone(Field):
    """
    Class for storing a phone number. Inherits from Field.
    Validates the phone number format (10 digits).
    """

    def __init__(self, value: str):
        """
        Initializes the phone number with validation.

        Args:
            value (str): The phone number.

        Raises:
            ValueError: If the phone number does not match the format (10 digits).
        """
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    """
    Class for storing and validating a birthday. Inherits from Field.
    """

    def __init__(self, value: str):
        """
        Initializes the birthday with validation.

        Args:
            value (str): The birthday in the format "DD.MM.YYYY".

        Raises:
            ValueError: If the birthday does not match the required format.
        """
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value):
            raise ValueError("Date must be in format: DD.MM.YYYY")
        try:
            birthday = self.convert_str_to_date(value)
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @staticmethod
    def convert_str_to_date(date: str) -> datetime.date:
        """
        Convert date string to date object.

        Args:
            date (str): The date string in the format "DD.MM.YYYY".

        Returns:
            datetime.date: The corresponding date object.
        """
        return datetime.strptime(date, "%d.%m.%Y").date()

    def __str__(self) -> str:
        """
        Returns a string representation of the birthday.

        Returns:
            str: The birthday in the format "DD.MM.YYYY".
        """
        return f"Birthday: {self.value.strftime('%d.%m.%Y')}"


class Record:
    """
    Class for storing contact information, including name, phone numbers, and birthday.

    Attributes:
        name (Name): The contact's name.
        phones (list of Phone): The contact's phone numbers.
        birthday (Birthday): The contact's birthday.
    """

    def __init__(self, name: str):
        """
        Initializes the record with the contact's name.

        Args:
            name (str): The contact's name.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthday to the record.

        Args:
            birthday (str): The birthday to add.
        """
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        """
        Adds a phone number to the record.

        Args:
            phone_number (str): The phone number to add.
        """
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """
        Removes a phone number from the record.

        Args:
            phone_number (str): The phone number to remove.
        """
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """
        Edits a phone number in the record.

        Args:
            old_number (str): The old phone number.
            new_number (str): The new phone number.
        """
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            if not re.fullmatch(r"\d{10}", new_number):
                raise ValueError("Phone number must be 10 digits")
            phone_to_edit.value = new_number

    def find_phone(self, phone_number: str) -> Phone:
        """
        Finds a phone number in the record.

        Args:
            phone_number (str): The phone number to find.

        Returns:
            Phone: The phone number if found, or None.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        """
        Returns a string representation of the record.

        Returns:
            str: The string representation of the record.
        """
        phone_list = '; '.join(p.value for p in self.phones)
        birthday_str = f", {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_list}{birthday_str}"


class AddressBook(UserDict):
    """
    Class for storing and managing contact records. Inherits from UserDict.
    """

    def add_record(self, record: Record) -> None:
        """
        Adds a record to the address book.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Finds a record by name in the address book.

        Args:
            name (str): The name to search for.

        Returns:
            Record: The record if found, or None.
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Deletes a record by name from the address book.

        Args:
            name (str): The name of the record to delete.
        """
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """
        Returns a list of users with upcoming birthdays, including the congratulation date.

        Returns:
            list[dict[str, str]]: List of users with upcoming birthdays.
        """
        users_upcoming_birthday = []
        today = datetime.today().date()
        for user_name, user in self.data.items():
            if user.birthday:
                birthday_date = user.birthday.value

                # Set the birthday to the current year
                birthday_this_year = birthday_date.replace(year=today.year)

                # If the birthday this year has already passed, set it to next year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # Check if the birthday is within the next 7 days
                if 0 <= (birthday_this_year - today).days <= 7:
                    # Adjust the birthday to avoid weekends
                    while birthday_this_year.weekday() in [5, 6]:
                        birthday_this_year += timedelta(days=1)
                    users_upcoming_birthday.append(
                        {
                            "name": user_name,
                            "congratulation_date": birthday_this_year.strftime("%d.%m.%Y"),
                        }
                    )

        return users_upcoming_birthday



# Usage Example

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
