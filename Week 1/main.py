import json
import time


# Load and Save functions
def load_contacts(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist
    except json.JSONDecodeError:
        print("Error decoding JSON from file.")
        return {}


def save_contacts(filename, contact_book):
    with open(filename, 'w') as file:
        json.dump(contact_book, file, indent=4)


# Main code
def clear_terminal():
    print("\n" * 2)


def add_contact():
    contact_name = input("Enter contact name: ").strip().lower()
    if not contact_name:
        print("Contact name cannot be empty.")
        return
    contact_number = input("Enter mobile number: ").strip()
    if not contact_number.isdigit():
        print("Invalid number. Please enter only digits.")
        return
    contact_email = input("Enter email address: ").strip()

    if contact_name in contact_book:
        if (contact_book[contact_name].get("number") == contact_number or
                contact_book[contact_name].get("email") == contact_email):
            print("Contact already found.")
        else:
            print(f"A contact with the name '{contact_name}' already exists but with a different number/email.")
            update_choice = input("Do you want to update the number or email?: ").strip().lower()
            if update_choice == "number":
                contact_book[contact_name]["number"] = contact_number
                print(f"Contact number for '{contact_name}' updated successfully!")
            elif update_choice == "email":
                contact_book[contact_name]["email"] = contact_email
                print(f"Contact Email for '{contact_name}' updated successfully!")
            else:
                print("Contact not updated.")
    else:
        # Check for duplicate number or email across all contacts
        for name, details in contact_book.items():
            if details.get("number") == contact_number:
                print(f"A contact with the number '{contact_number}' already exists.")
                return
            if details.get("email") == contact_email:
                print(f"A contact with the email '{contact_email}' already exists.")
                return
        contact_book[contact_name] = {"number": contact_number, "email": contact_email}
        print("Contact added successfully!")
    save_contacts(contact_file, contact_book)


def list_contact():
    if not contact_book:
        print("No contacts found. Add some contacts.")
    else:
        for name, details in contact_book.items():
            print(f"Name: {name.capitalize()}")
            print(f"Number: {details['number']}")
            print(f"Email: {details['email']}")


def view_contact():
    contact_name = input("Enter the name of the contact you want to view: ").strip().lower()
    if contact_name in contact_book:
        print(f"Name: {contact_name.capitalize()}")
        print(f"Number: {contact_book[contact_name]['number']}")
        print(f"Email: {contact_book[contact_name]['email']}")
    else:
        print(f"No contact found for the name '{contact_name}'. You can add them using the 'add' option.")


def edit_contact():
    contact_name = input("Enter the name of the contact you want to update: ").strip().lower()
    if contact_name in contact_book:
        data = input("Enter the data you want to change [name, number, email]: ").strip().lower()
        value = input(f"Enter the new {data}: ").strip().lower()

        if data == "name":
            if value in contact_book:
                print(f"A contact with the name '{value}' already exists.")
                return
            contact_book[value] = contact_book.pop(contact_name)
            print("Contact name updated successfully!")
        elif data == "number":
            # Check if the number already exists
            for contact in contact_book.values():
                if contact.get("number") == value:
                    print(f"The number '{value}' is already associated with another contact.")
                    return
            contact_book[contact_name]["number"] = value
            print("Contact number updated successfully!")
        elif data == "email":
            # Check if the email already exists
            for contact in contact_book.values():
                if contact.get("email") == value:
                    print(f"The email '{value}' is already associated with another contact.")
                    return
            contact_book[contact_name]["email"] = value
            print("Contact email updated successfully!")
        else:
            print(f"Invalid data choice: '{data}'. Please enter 'name', 'number', or 'email'.")
        save_contacts(contact_file, contact_book)
    else:
        print(f"No contact found for the name '{contact_name}'.")


def delete_contact():
    contact_name = input("Enter contact name to be deleted: ").strip().lower()
    if contact_name in contact_book:
        del contact_book[contact_name]
        print("Contact successfully deleted.")
        save_contacts(contact_file, contact_book)
    else:
        print(f"No contact found for the name '{contact_name}'.")


close = False
contact_file = 'contacts.json'
contact_book = load_contacts(contact_file)
print("Opening your Contacts..")

while not close:
    time.sleep(2)
    clear_terminal()
    print("Welcome to your contact book.")
    print("> Enter 'add' to Add contact")
    print("> Enter 'view' to View contact")
    print("> Enter 'edit' to Edit contact")
    print("> Enter 'delete' to Delete contact")
    print("> Enter 'show' to List all your contacts")
    print("> Enter 'close' to Exit")

    user_input = input("What would you like to do: ").strip().lower()

    if user_input == "add":
        add_contact()
    elif user_input == "show":
        list_contact()
    elif user_input == "edit":
        edit_contact()
    elif user_input == "delete":
        delete_contact()
    elif user_input == "view":
        view_contact()
    elif user_input == "close":
        close = True
        save_contacts(contact_file, contact_book)
        print("You have exited.")
    else:
        print("Invalid input, please try again.")
