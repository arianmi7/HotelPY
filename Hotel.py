import json
import os
import sys


USER_FILE = "users.json"
ROOMS_FILE = "rooms_data.json"
ADMIN_PASSWORD = "2005"  

print("\n-----Hello welcome to Arian Hotel-----\n")

def menu():
    while True:
        print("-/-/-/-/-/-/-/-/-/")
        print("1. Guest User")
        print("2. Hotel User")
        print("3. About us")
        print("4. Exit")
        print("-/-/-/-/-/-/-/-/-/")
        choice = input("Enter Your Choice: ")

        if choice == '1':
            guest_menu()
        elif choice == '2':
            hotel_menu()
        elif choice == '3':
            print(about_us())
        elif choice == '4':
            print("\n...Thank You For Choosing Arian Hotel...\n")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def hotel_menu():
    print("-------------------------")
    password = input("Enter Admin Password: ")
    print("-------------------------")

    if password == ADMIN_PASSWORD:
        admin_menu()
    else:
        print("The Password is Incorrect, The Program Will Close.")
        sys.exit()

def admin_menu():
    while True:
        print("--\\\ADMIN--MENU///--")
        print("1. Rooms Data")
        print("2. User Data")
        print("3. Back to main menu")

        choice = input("Choice: ")
        if choice == "1":
            show_all_rooms()
        elif choice == "2":
            show_user_inputs()
        elif choice == "3":
            menu()
        else:
            print("pls enter 1,2,3")

def show_all_rooms(filename):
    print("\n*** rooms List ***")
    if not os.path.exists(filename):
        print("no rooms registered yet.") 
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            rooms = data.get("rooms", [])

            if not rooms:
                print("No rooms found in the file.")
                return

            for room in rooms:
                print(f"\nRoom ID: {room.get('id')}")
                print(f"  Name: {room.get('name')}")
                print(f"  Floor: {room.get('floor')}")
                print(f"  Beds: {room.get('beds')}")
                print(f"  View: {room.get('view')}")
                print(f"  Price per Night: {room.get('price')} units")
                print(f"  Features: {', '.join(room.get('options', []))}")
                print(f"  Status: {'Available' if not room.get('reserved') else 'Reserved'}")
    except FileNotFoundError:
        print(f" The file '{filename}' was not found.")
    

def show_user_inputs():
    users = load_users()
    if not users:
        print("There are no users registered!")
    else:
        print("\n*** User List ***")
        for national_code, data in users.items():
            print(f"\nNational Code: {national_code}")
            print(f"  Name: {data.get('name')}")
            print(f"  Family: {data.get('family')}")


def guest_menu():
    while True:
        print("-------------------------")
        print("1. Login")
        print("2. Create An Account")
        print("3. Back to Main Menu")
        print("-------------------------")

        choice = input("Your Choice: ")

        if choice == '1':
           user = login_users()
        elif choice == '2':
            new_account()
        elif choice == '3':
            menu()
        else:
            print("Invalid Choice...!")


def load_users():
    try: 
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                content = f.read() 
                if content: 
                    return json.loads(content) 
                else:
                    return {} 
        else:
            return {}
    except FileNotFoundError:
        print(f"The user file '{USER_FILE}' was not found.")
        return {}


def save_users(users):
    try: 
        with open(USER_FILE, 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")


def load_rooms():
    try:
        with open('rooms_data.json', 'r') as file:
            rooms = json.load(file)
            return rooms
    except:
        return {}
    
def save_rooms(rooms):
    try:
        with open(ROOMS_FILE, 'w', encoding='utf-8') as file:
            json.dump(rooms, file, indent=4)
    except Exception as e:
        print(f"Error Saving room data: {e}")


def new_account():
    print("Please Enter Your Profile:")
    name = input("Your Name: ")
    family = input("Family: ")
    national_code = input("National Code: ")
    password = input("Create a Password: ")

    users = load_users()

    if national_code in users:
        print("This National Code has already been used.")
        return

    
    users[national_code] = {
        "password": password,
        "family": family,
        "name": name,
        "national_code": national_code 
    }

    save_users(users)
    print("Account Created Successfully...")
    return reserved_rooms(national_code)

def reserved_rooms(national_code):
    rooms = load_rooms()
    print("\nAvalible Rooms: ")
    for room_id, info in rooms.items():
        if not info.get('reserved', False):
            print(f"Room ID: {room_id}, info: {info}")

    selected_room = input("Enter The Room ID To Reserved: ")

    if selected_room in rooms and not rooms[selected_room].get('reserved', False):
        rooms[selected_room]['reserved'] = True

        users = load_users()
        users[national_code]['room'] = selected_room

        save_users(users)
        save_rooms(rooms)

        print(f"Room {selected_room} reserved successfully!")
    else:
        print("invalid or alredy reserved room.!!")


def login_users():
    users = load_users()
    national_code = input("National Code: ")
    password = input("Password: ")

    if national_code in users and users[national_code]['password'] == password:
        print(f"Login successful... Welcome {users[national_code]['name']} {users[national_code]['family']}")
        user = {
            'national_code': national_code,
            'data': users[national_code]
        }
        user_panel(user)
    else:
        print("Invalid National Code or password...!")
        return None


def user_panel(user):
    while True:
        user_data = user['data']
        print(f"----Welcome {user_data.get('name', '')} {user_data.get('family', '')}----")
        print("1. View Profile")
        print("2. Logout")
        choice = input("Enter Your Choice: ")

        if choice == '1':
            print("\n--- Your Profile ---")
            print(f"Name: {user_data.get('name')}")
            print(f"Family: {user_data.get('family')}")
            print(f"National Code: {user_data.get('national_code')}") 
            print(f"Reserved Room: {user_data.get('room', 'None')}")
          
        elif choice == '2':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")


def about_us():
    return """
    This hotel management software was developed by Arian Miraki.
    All material and intellectual property rights of this program belong to him.
    Year of creation: 2025
    """


if __name__ == "__main__":
    menu()