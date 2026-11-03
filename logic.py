from cryptography.fernet import Fernet
from pathlib import Path
import machineid

def get_parent_path():
    file_name = "logic.py"
    root_dir = Path(".")

    # Loops through and finds the parent directory
    found_files = list(root_dir.rglob(file_name))

    if found_files:
        file_path = found_files[0]
        parent_dir = file_path.parent
        return parent_dir
    else:
        return 0

def check_machine_cookies():
    machine_id = machineid.id()

    logged_in = False

    with open(f"{get_parent_path()}/cookies.txt", "r") as cookies_file:
        for line in cookies_file.readlines():
            machine, username = line.strip().split(" $^&^$ ")
            if machine == machine_id:
                logged_in = username
        cookies_file.close()

    return logged_in

def save_machine_cookies(username):
    machine_id = machineid.id()

    with open(f"{get_parent_path()}/cookies.txt", "a") as cookies_file:
        cookies_file.write(f"{machine_id} $^&^$ {username}")
        cookies_file.close()

def reset_status():
    with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
        return_file.write("")  # Clear the contents of the file

def generate_key():
    key = Fernet.generate_key()
    with open(f"{get_parent_path()}/secret.key", "wb") as key_file:
        key_file.write(key)


def handle_login(username, password):
    with open (f"{get_parent_path()}/secret.key", "rb") as key_file:
        key = key_file.read()
        key_file.close()
    
    cipher_suite = Fernet(key)

    with open(f"{get_parent_path()}/accounts.txt", "r") as f:
        found_username = False
        for line in f:
            stored_username, stored_encrypted_password = line.strip().split(" %!-|\%/|-!% ")
            if stored_username == username:
                found_username = True
                decrypted_password = cipher_suite.decrypt(stored_encrypted_password.encode()).decode()
                if decrypted_password == password:
                    save_machine_cookies(username)
                    with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
                        return_file.write("Login successful")
                        return_file.close()
                    return "Login successful"
                    f.close()
                else:
                    with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
                        return_file.write("Incorrect password")
                        return_file.close()
                    return "Incorrect password"
                    f.close()

        if not found_username:
            with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
                return_file.write(f"No user '{username}' exists")
                return_file.close()
            f.close()
            return f"No user '{username}' exists"

def handle_signup(username, password, password_confirm):
    if password != password_confirm:
        with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
            return_file.write("Passwords do not match")
            return_file.close()
        return "Passwords do not match"

    with open(f"{get_parent_path()}/secret.key", "rb") as key_file: 
        key = key_file.read()
        key_file.close()

    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())

    with open(f"{get_parent_path()}/accounts.txt", "r") as f:
        for line in f:
            stored_username, _ = line.strip().split(" %!-|\%/|-!% ")
            if stored_username == username:
                with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
                    return_file.write("Username already exists")
                    return_file.close()
                f.close()
                return "Username already exists"

    with open(f"{get_parent_path()}/accounts.txt", "a") as f:
        f.write(f"{username} %!-|\%/|-!% {encrypted_password.decode('ascii')}\n")
        with open(f"{get_parent_path()}/returns.txt", "w") as return_file:
            save_machine_cookies(username)
            return_file.write("Sign up successful")
            return_file.close()
        f.close()