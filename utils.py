import csv

# Імена CSV-файлів для зберігання даних
THERMOMETERS_CSV = 'thermometers.csv'
CATEGORIES_CSV = 'categories.csv'
PROPERTIES_CSV = 'properties.csv'
USERS_CSV = 'users.csv'

# Функція для збереження користувачів у CSV
def save_users_to_csv(users):
    with open(USERS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])
        for username, password in users.items():
            writer.writerow([username, password])

# Функція для завантаження користувачів з CSV
def load_users_from_csv():
    users = {}
    try:
        with open(USERS_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = row['password']
    except FileNotFoundError:
        pass
    return users

# Функція для збереження термометрів у CSV
def save_thermometers_to_csv(thermometers):
    with open(THERMOMETERS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'vendor', 'category', 'min_temp', 'max_temp', 'accuracy'])
        for thermo in thermometers:
            writer.writerow([thermo['name'], thermo['vendor'], thermo['category'], thermo['min_temp'], thermo['max_temp'], thermo['accuracy']])

# Функція для завантаження термометрів з CSV
def load_thermometers_from_csv():
    thermometers = []
    try:
        with open(THERMOMETERS_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                thermometers.append({
                    'name': row['name'],
                    'vendor': row['vendor'],
                    'category': row['category'],
                    'min_temp': row['min_temp'],
                    'max_temp': row['max_temp'],
                    'accuracy': row['accuracy']
                })
    except FileNotFoundError:
        pass
    return thermometers

# Функція для збереження категорій у CSV
def save_categories_to_csv(categories):
    with open(CATEGORIES_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name'])
        for category in categories:
            writer.writerow([category['name']])

# Функція для завантаження категорій з CSV
def load_categories_from_csv():
    categories = []
    try:
        with open(CATEGORIES_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                categories.append({'name': row['name']})
    except FileNotFoundError:
        pass
    return categories

# Функція для збереження властивостей у CSV
def save_properties_to_csv(properties):
    with open(PROPERTIES_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'units'])
        for prop in properties:
            writer.writerow([prop['name'], prop['units']])

# Функція для завантаження властивостей з CSV
def load_properties_from_csv():
    properties = []
    try:
        with open(PROPERTIES_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                properties.append({'name': row['name'], 'units': row['units']})
    except FileNotFoundError:
        pass
    return properties
