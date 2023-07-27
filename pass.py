import hashlib
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password.encode()
        self.passwords = {}
        self.key = None

    def _generate_key(self):
        hash_object = hashlib.sha256(self.master_password)
        self.key = hash_object.digest()

    def _encrypt(self, data):
        if not self.key:
            self._generate_key()
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    def _decrypt(self, encrypted_data):
        if not self.key:
            self._generate_key()
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data

    def add_password(self, website, username, password):
        encrypted_username = self._encrypt(username)
        encrypted_password = self._encrypt(password)
        self.passwords[website] = {
            'username': encrypted_username,
            'password': encrypted_password
        }

    def get_password(self, website):
        if website in self.passwords:
            encrypted_username = self.passwords[website]['username']
            encrypted_password = self.passwords[website]['password']
            username = self._decrypt(encrypted_username)
            password = self._decrypt(encrypted_password)
            return username, password
        else:
            return None

    def list_websites(self):
        return list(self.passwords.keys())

if __name__ == "__main__":
    print("Welcome to the Password Manager!")
    master_password = input("Please enter your master password: ")
    password_manager = PasswordManager(master_password)

    while True:
        print("\nOptions:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. List stored websites")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            website = input("Enter the website name: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            password_manager.add_password(website, username, password)
            print("Password added successfully!")
        elif choice == '2':
            website = input("Enter the website name: ")
            credentials = password_manager.get_password(website)
            if credentials:
                username, password = credentials
                print(f"Username: {username}\nPassword: {password}")
            else:
                print("Website not found in the password manager.")
        elif choice == '3':
            websites = password_manager.list_websites()
            if websites:
                print("Stored websites:")
                for website in websites:
                    print(website)
            else:
                print("No websites stored in the password manager.")
        elif choice == '4':
            print("Exiting the Password Manager.")
            break
        else:
            print("Invalid choice. Please try again.")
