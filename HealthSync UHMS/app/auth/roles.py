# app/auth/roles.py

# Role constants
ROLE_ADMIN = "admin"
ROLE_PATIENT = "patient"

def get_all_roles():
    return [ROLE_ADMIN, ROLE_PATIENT]
