import os
from flask import Flask, request, jsonify, session as flask_session
from flask_cors import CORS
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from database.tables import User, Thermometer, Category, Property

# Ініціалізація Flask додатку
app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

DB_URI = os.environ.get('DATABASE_URI', 'postgresql+psycopg2://postgres:changeme@localhost:5432/thermometers')

# Підключення до бази даних PostgreSQL
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()


def initialize_data():
    # Перевірка та додавання користувачів
    if db_session.query(User).count() == 0:
        User.add_user("admin", "password123")
        User.add_user("user1", "mypassword")
        print("Users added")

    # Перевірка та додавання категорій
    if db_session.query(Category).count() == 0:
        Category.add("Електронні термометри")
        Category.add("Інфрачервоні термометри")
        print("Categories added")

    # Перевірка та додавання властивостей
    if db_session.query(Property).count() == 0:
        Property.add("Точність", "°C")
        Property.add("Діапазон температур", "°C")
        print("Properties added")

    # Перевірка та додавання термометрів
    if db_session.query(Thermometer).count() == 0:
        Thermometer.add(
            name="ThermoPro TP-50",
            vendor="ThermoPro",
            category_name="Електронні термометри",
            min_temp=-50,
            max_temp=70,
            accuracy=0.1,
            property_names=["Точність", "Діапазон температур"]
        )

        Thermometer.add(
            name="Braun Thermoscan",
            vendor="Braun",
            category_name="Інфрачервоні термометри",
            min_temp=-20,
            max_temp=60,
            accuracy=0.2,
            property_names=["Точність"]
        )
        print("Thermometers added")

# Викликаємо функцію ініціалізації при запуску програми
initialize_data()





# Ендпоінти для моделі User

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if db_session.query(User).filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, password=password)
    db_session.add(user)
    db_session.commit()
    return jsonify({"message": "User created", "user": {"username": username}}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = db_session.query(User).all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username})
    return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    User.update_by_id(user_id, username=username, password=password)
    return jsonify({"message": "User updated"})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete_by_id(user_id)
    return jsonify({"message": "User deleted"})

@app.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '').strip()
    results_query = db_session.query(User).filter(
        User.username.ilike(f"%{query}%")
    )
    results = results_query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username
    } for user in results])

# Ендпоінт для автентифікації
@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = db_session.query(User).filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Authenticated", "user": {"username": username}})
    return jsonify({"error": "Invalid credentials"}), 401


# Ендпоінти для моделі Category

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    category = Category(name=name)
    db_session.add(category)
    db_session.commit()
    return jsonify({"message": "Category created", "category": {"id": category.id, "name": name}}), 201



@app.route('/categories', methods=['GET'])
def get_categories():
    categories = db_session.query(Category).all()
    return jsonify([{"id": category.id, "name": category.name} for category in categories])


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_single_category(category_id):
    category = Category.get_by_id(category_id)
    if category:
        return jsonify({"id": category.id, "name": category.name})
    return jsonify({"error": "Category not found"}), 404


@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    name = data.get('name')
    Category.update_by_id(category_id, name=name)
    return jsonify({"message": "Category updated"})


@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    Category.delete_by_id(category_id)
    return jsonify({"message": "Category deleted"})


@app.route('/categories/search', methods=['GET'])
def search_categories():
    query = request.args.get('query', '').strip()
    results_query = db_session.query(Category).filter(
        Category.name.ilike(f"%{query}%")
    )
    results = results_query.all()
    return jsonify([{
        "id": category.id,
        "name": category.name
    } for category in results])

# Ендпоінти для моделі Property

@app.route('/properties', methods=['POST'])
def add_property():
    data = request.get_json()
    name = data.get('name')
    units = data.get('units')
    property = Property(name=name, units=units)
    db_session.add(property)
    db_session.commit()
    return jsonify({"message": "Property created", "property": {"id": property.id, "name": name, "units": units}}), 201


@app.route('/properties', methods=['GET'])
def get_properties():
    properties = db_session.query(Property).all()
    return jsonify([{"id": prop.id, "name": prop.name, "units": prop.units} for prop in properties])


@app.route('/properties/<int:property_id>', methods=['GET'])
def get_single_property(property_id):
    property_instance = Property.get_by_id(property_id)
    if property_instance:
        return jsonify({"id": property_instance.id, "name": property_instance.name, "units": property_instance.units})
    return jsonify({"error": "Property not found"}), 404

@app.route('/properties/search', methods=['GET'])
def search_properties():
    query = request.args.get('query', '').strip()
    results_query = db_session.query(Property).filter(
        (Property.name.ilike(f"%{query}%")) |
        (Property.units.ilike(f"%{query}%"))
    )
    results = results_query.all()
    return jsonify([{
        "id": prop.id,
        "name": prop.name,
        "units": prop.units
    } for prop in results])

@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    data = request.get_json()
    name = data.get('name')
    units = data.get('units')
    Property.update_by_id(property_id, name=name, units=units)
    return jsonify({"message": "Property updated"})


@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    Property.delete_by_id(property_id)
    return jsonify({"message": "Property deleted"})

# Ендпоінти для моделі Thermometer

@app.route('/thermometers', methods=['POST'])
def add_thermometer():
    data = request.get_json()
    name = data.get('name')
    vendor = data.get('vendor')
    category_name = data.get('category')
    min_temp = data.get('min_temp')
    max_temp = data.get('max_temp')
    accuracy = data.get('accuracy')
    property_names = data.get('properties', [])

    category = db_session.query(Category).filter_by(name=category_name).first()
    if not category:
        return jsonify({"error": "Category not found"}), 400

    properties = db_session.query(Property).filter(Property.name.in_(property_names)).all()
    thermometer = Thermometer(
        name=name,
        vendor=vendor,
        category=category,
        min_temp=min_temp,
        max_temp=max_temp,
        accuracy=accuracy,
        properties=properties
    )
    db_session.add(thermometer)
    db_session.commit()
    return jsonify({"message": "Thermometer created", "thermometer": {
        "id": thermometer.id,
        "name": name,
        "vendor": vendor,
        "category": category.name,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "accuracy": accuracy,
        "properties": property_names
    }}), 201


@app.route('/thermometers', methods=['GET'])
def get_thermometers():
    thermometers = db_session.query(Thermometer).all()
    return jsonify([{
        "id": thermo.id,
        "name": thermo.name,
        "vendor": thermo.vendor,
        "category": thermo.category.name,
        "min_temp": thermo.min_temp,
        "max_temp": thermo.max_temp,
        "accuracy": thermo.accuracy,
        # "properties": [prop.name for prop in thermo.properties]
    } for thermo in thermometers])


@app.route('/thermometers/<int:thermometer_id>', methods=['GET'])
def get_single_thermometer(thermometer_id):
    thermometer = Thermometer.get_by_id(thermometer_id)
    if thermometer:
        return jsonify({
            "id": thermometer.id,
            "name": thermometer.name,
            "vendor": thermometer.vendor,
            "category": thermometer.category.name,
            "min_temp": thermometer.min_temp,
            "max_temp": thermometer.max_temp,
            "accuracy": thermometer.accuracy,
            "properties": [prop.name for prop in thermometer.properties]
        })
    return jsonify({"error": "Thermometer not found"}), 404


@app.route('/thermometers/<int:thermometer_id>', methods=['PUT'])
def update_thermometer(thermometer_id):
    data = request.get_json()
    name = data.get('name')
    vendor = data.get('vendor')
    min_temp = data.get('min_temp')
    max_temp = data.get('max_temp')
    accuracy = data.get('accuracy')
    property_names = data.get('properties', [])
    category_name = data.get('category')

    category = db_session.query(Category).filter_by(name=category_name).first() if category_name else None
    property_ids = [prop.id for prop in db_session.query(Property).filter(Property.name.in_(property_names)).all()]

    Thermometer.update_by_id(
        thermometer_id, name=name, vendor=vendor, category_id=category.id if category else None,
        min_temp=min_temp, max_temp=max_temp, accuracy=accuracy, property_ids=property_ids
    )
    return jsonify({"message": "Thermometer updated"})


@app.route('/thermometers/<int:thermometer_id>', methods=['DELETE'])
def delete_thermometer(thermometer_id):
    Thermometer.delete_by_id(thermometer_id)
    return jsonify({"message": "Thermometer deleted"})


@app.route('/thermometers/search', methods=['GET'])
def search_thermometers():
    query = request.args.get('query', '').strip()
    print("QUERY: ", query)
    # Базовий запит
    results_query = db_session.query(Thermometer).join(Category).filter(
        (Thermometer.name.ilike(f"%{query}%")) |
        (Thermometer.vendor.ilike(f"%{query}%")) |
        (Category.name.ilike(f"%{query}%"))
    )

    # Виконання запиту
    results = results_query.all()

    # Формування JSON відповіді
    return jsonify([{
        "id": thermo.id,
        "name": thermo.name,
        "vendor": thermo.vendor,
        "category": thermo.category.name,
        "min_temp": thermo.min_temp,
        "max_temp": thermo.max_temp,
        "accuracy": thermo.accuracy,
        "properties": [prop.name for prop in thermo.properties]
    } for thermo in results])


# Ендпоінт для входу
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db_session.query(User).filter_by(username=username, password=password).first()
    if user:
        flask_session['user_id'] = user.id  # Зберігаємо ID користувача в сесії Flask
        flask_session['username'] = user.username
        return jsonify({"message": "Successfully logged in", "username": user.username}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# Ендпоінт для виходу
@app.route('/logout', methods=['POST'])
def logout():
    flask_session.pop('user_id', None)
    flask_session.pop('username', None)
    return jsonify({"message": "Successfully logged out"}), 200


# Ендпоінт для перевірки статусу авторизації
@app.route('/status', methods=['GET'])
def status():
    if 'user_id' in flask_session:
        return jsonify({"authenticated": True, "username": flask_session['username']}), 200
    else:
        return jsonify({"authenticated": False}), 401


# Запуск Flask додатку
if __name__ == '__main__':
    app.run(debug=True)
