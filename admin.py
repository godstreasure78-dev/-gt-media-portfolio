import sqlite3
from werkzeug.security import generate_password_hash
import getpass

DATABASE = "gt_media.db"

username = input("Enter admin username: ").strip()
password = getpass.getpass("Enter admin password: ")
confirm = getpass.getpass("Confirm admin password: ")

if password != confirm:
    print("❌ Passwords do not match.")
    exit()

if not username or not password:
    print("❌ Username and password cannot be empty.")
    exit()

password_hash = generate_password_hash(password)

connection = sqlite3.connect(DATABASE)

try:
    connection.execute(
        "INSERT INTO admins (username, password) VALUES (?, ?)",
        (username, password_hash)
    )

    connection.commit()
    print("✅ Admin account created successfully!")

except sqlite3.IntegrityError:
    print("❌ That username already exists.")

finally:
    connection.close()