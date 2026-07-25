"""
schema.py

Contains all constants required for generating synthetic cybersecurity
behavioral datasets for SentinelAI.
"""

# ==========================
# USER ROLES
# ==========================

USER_ROLES = [
    "Engineer",
    "HR",
    "Finance",
    "Admin",
    "IT Support",
]

# ==========================
# DEPARTMENTS
# ==========================

DEPARTMENTS = [
    "Engineering",
    "Human Resources",
    "Finance",
    "IT",
    "Security",
]

ROLE_TO_DEPARTMENT = {
    "Engineer": "Engineering",
    "HR": "Human Resources",
    "Finance": "Finance",
    "Admin": "IT",
    "IT Support": "Security",
}

# ==========================
# COUNTRIES & CITIES
# ==========================

COUNTRY_CITY_MAP = {
    "India": [
        "Bangalore",
        "Mumbai",
        "Pune",
        "Hyderabad",
    ],
    "USA": [
        "New York",
        "Seattle",
        "Austin",
    ],
    "Germany": [
        "Berlin",
        "Munich",
    ],
    "UK": [
        "London",
        "Manchester",
    ],
    "Singapore": [
        "Singapore",
    ],
}

COUNTRIES = list(COUNTRY_CITY_MAP.keys())

# Flatten all cities
CITIES = []
for city_list in COUNTRY_CITY_MAP.values():
    CITIES.extend(city_list)

# ==========================
# DEVICES
# ==========================

DEVICE_TYPES = [
    "Laptop",
    "Desktop",
    "Mobile",
]

# ==========================
# BROWSERS
# ==========================

BROWSERS = [
    "Chrome",
    "Edge",
    "Firefox",
]

# ==========================
# OPERATING SYSTEMS
# ==========================

OPERATING_SYSTEMS = [
    "Windows",
    "Linux",
    "macOS",
]

# ==========================
# AUTH METHODS
# ==========================

AUTH_METHODS = [
    "Password",
    "MFA",
    "SSO",
]

# ==========================
# DEPARTMENT RESOURCES
# ==========================

DEPARTMENT_RESOURCES = {
    "Engineering": [
        "GitHub",
        "Jira",
        "VPN",
        "Database",
        "Email",
    ],
    "Human Resources": [
        "HR Portal",
        "Email",
        "ERP",
    ],
    "Finance": [
        "ERP",
        "Database",
        "Email",
    ],
    "IT": [
        "VPN",
        "Database",
        "Email",
    ],
    "Security": [
        "VPN",
        "Database",
        "GitHub",
        "Email",
    ],
}

# Master resource list

RESOURCES = sorted(
    {
        resource
        for values in DEPARTMENT_RESOURCES.values()
        for resource in values
    }
)

# ==========================
# ATTACK TYPES
# ==========================

ATTACK_TYPES = [
    "Normal",
    "Brute Force",
    "Impossible Travel",
    "Credential Stuffing",
    "Device Spoofing",
    "Insider Threat",
    "Lateral Movement",
]

# ==========================
# ATTACK DISTRIBUTION
# ==========================

ATTACK_DISTRIBUTION = {
    "Brute Force": 0.02,
    "Impossible Travel": 0.02,
    "Credential Stuffing": 0.015,
    "Device Spoofing": 0.015,
    "Insider Threat": 0.01,
    "Lateral Movement": 0.01,
}

# ==========================
# LOGIN HOURS
# ==========================

NORMAL_LOGIN_START = 8
NORMAL_LOGIN_END = 18

# ==========================
# SESSION DURATIONS
# ==========================

MIN_SESSION_DURATION = 20
MAX_SESSION_DURATION = 90

# ==========================
# RANDOM SEED
# ==========================

RANDOM_SEED = 42