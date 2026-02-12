from datetime import datetime
import json
import sys
import os

# --- File setup using os ---
BASE_DIR = "basic_model"
FILE_PATH = os.path.join(BASE_DIR, "basic_model.json")


def load_users():
    if not os.path.isfile(FILE_PATH):
        return {}

    with open(FILE_PATH, 'r') as f:
        return json.load(f)


def save_users(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def send_message(user_logins, sender):
    recipient = input("Enter the username of the person you want to message: ")
    msg = input("\nEnter your message: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if recipient in user_logins:
        print(f"Message sent to {recipient} at {timestamp}: {msg}")

        user_logins[recipient]["Message"] = {
            "from": sender,
            "text": msg,
            "time": timestamp
        }

        save_users(user_logins)

    else:
        print("Recipient not found. Double check for a typo and try again.")


def run():
    print("Hello, I am a terminal-based messaging app!")
    print("In order to message someone, you need to sign up first.")

    sign_up_step = input("[1] Sign Up [2] Log In [3] Exit  ")

    user_logins = load_users()

    # SIGN UP
    if sign_up_step == "1":
        username = input("Enter your username: ")
        pin = int(input("Enter your pin/numerical password: "))
        

        user_logins[username] = {
            "Pin": pin,
            "Message": {
                "from": "",
                "text": "",
                "time": ""
            }
        }

        save_users(user_logins)

        print(f"User {username} signed up successfully!")

        print("You can now log in to send messages."); run()

    # LOG IN
    elif sign_up_step == "2":
        username = input("Enter your username: ")
        pin = int(input("Enter your pin: "))

        if username in user_logins and user_logins[username]["Pin"] == pin:
            print(f"Welcome back, {username}!")
            action = input("What would you like to do? [1] Send a message [2] View messages [3] Exit  ")

            if action == "1":
                send_message(user_logins, username)

            elif action == "2":
                try:
                    msg_data = user_logins[username]["Message"]
                    print(f"{msg_data['from']} sent you '{msg_data['text']}' at {msg_data['time']}")

                except TypeError:
                    print("You have no messages.")

            elif action == "3":
                print("Goodbye!")
                sys.exit()

            else:
                print("Pick the right step")
                run()

        else:
            print("Invalid username or pin. Please try again.")

    # EXIT
    elif sign_up_step == "3":
        print("Goodbye!")
        sys.exit()

    else:
        print("Enter 1, 2 or 3 next time. Goodbye!")


run()