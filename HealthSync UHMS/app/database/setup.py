# app/database/setup.py

from app.auth.user_manager import create_user_table
# Add admin user if not exists
from app.auth.user_manager import register_user, user_exists
from app.auth.roles import ROLE_ADMIN

if not user_exists("admin"):
    register_user("admin", "admin123", role=ROLE_ADMIN)
    print("✅ Default admin account created.")

if __name__ == "__main__":
    create_user_table()
    print("✅ User table created.")
