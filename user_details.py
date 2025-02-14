import random
import string

# List of common first and last names
FIRST_NAMES = ["Alice", "John", "Emily", "Mark", "Olivia", "Daniel", "Sophia", "Ryan", "Michael", "Emma"]
LAST_NAMES = ["Smith", "Doe", "Johnson", "Williams", "Brown", "Clark", "White", "Taylor", "Davis", "Martinez"]

def generate_strong_password(length=15):
    """Generate a strong password with letters, digits, and special characters."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(chars, k=length))

def generate_fake_user():
    """Generate fake user details with a meaningful username."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    day = str(random.randint(1, 28))
    month = str(random.randint(1, 12))
    year = str(random.randint(1980, 2005))
    # New Username Format: firstnamelastnameDDMMYYYY
    username = f"{first_name.lower()}{last_name.lower()}{day}{month}{year}"

    password = generate_strong_password()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "day": day,
        "month": month,
        "year": year,
        "username": username,
        "password": password
    }
