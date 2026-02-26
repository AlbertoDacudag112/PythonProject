"""
migrate_passwords.py
One-time script to hash all existing plain-text passwords in the database.
Run this ONCE before deploying the updated UserModel.py.

Usage: python migrate_passwords.py
"""
import hashlib
import mysql.connector
from mysql.connector import Error


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def is_already_hashed(password: str) -> bool:
    """SHA-256 hashes are always exactly 64 hex characters"""
    return len(password) == 64 and all(c in '0123456789abcdef' for c in password.lower())


def migrate():
    # ── Update these if your DB credentials differ ──
    config = {
        'host': 'localhost',
        'database': 'RoadEyeDB',
        'user': 'root',
        'password': ''
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Fetch all users with their current passwords
        cursor.execute("SELECT UserID, Password FROM users")
        users = cursor.fetchall()

        migrated = 0
        skipped = 0

        for user_id, plain_password in users:
            if is_already_hashed(plain_password):
                print(f"  SKIP  {user_id} — already hashed")
                skipped += 1
            else:
                hashed = hash_password(plain_password)
                cursor.execute(
                    "UPDATE users SET Password = %s WHERE UserID = %s",
                    (hashed, user_id)
                )
                print(f"  HASH  {user_id} — password hashed successfully")
                migrated += 1

        conn.commit()
        cursor.close()
        conn.close()

        print(f"\n✅ Migration complete: {migrated} hashed, {skipped} skipped.")

    except Error as e:
        print(f"❌ Migration failed: {e}")


if __name__ == '__main__':
    print("Starting password migration...\n")
    migrate()