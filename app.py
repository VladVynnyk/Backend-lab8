from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

from utils import (
    load_properties_from_csv,
    save_properties_to_csv,
    load_thermometers_from_csv,
    save_thermometers_to_csv,
    save_users_to_csv, 
    load_users_from_csv, 
    load_categories_from_csv, 
    save_categories_to_csv
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Ініціалізація даних
users = load_users_from_csv()
thermo_list = load_thermometers_from_csv()
category_list = load_categories_from_csv()
property_list = load_properties_from_csv()


# Форма реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            return 'Користувач з таким іменем вже існує', 400
        
        users[username] = password
        save_users_to_csv(users)  # Зберігаємо користувача в CSV
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

# Форма входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Невірний логін або пароль', 401
    return render_template('login.html')

# Форма додавання термометра
@app.route('/add_thermometer', methods=['GET', 'POST'])
def add_thermometer():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        vendor = request.form['vendor']
        category = request.form['category']
        min_temp = request.form['min_temp']
        max_temp = request.form['max_temp']
        accuracy = request.form['accuracy']
        thermo_list.append({
            'name': name,
            'vendor': vendor,
            'category': category,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'accuracy': accuracy
        })
        save_thermometers_to_csv(thermo_list)  # Зберігаємо термометри в CSV
        return redirect(url_for('dashboard'))
    return render_template('add_thermometer.html')

# Форма додавання категорії
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        category_list.append({'name': name})
        save_categories_to_csv(category_list)  # Зберігаємо категорії в CSV
        return redirect(url_for('dashboard'))
    return render_template('add_category.html')

# Форма додавання властивості
@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        units = request.form['units']
        property_list.append({'name': name, 'units': units})
        save_properties_to_csv(property_list)  # Зберігаємо властивості в CSV
        return redirect(url_for('dashboard'))
    return render_template('add_property.html')

# Головна сторінка (панель керування)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', thermometers=thermo_list, categories=category_list, properties=property_list)

# Вихід із системи
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Запуск Flask додатку
if __name__ == '__main__':
    app.run(debug=True)
