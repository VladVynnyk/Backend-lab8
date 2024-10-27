from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:changeme@localhost:5432/thermometers', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

thermometer_property = Table(
    'thermometer_property', Base.metadata,
    Column('thermometer_id', Integer, ForeignKey('thermometers.id'), primary_key=True),
    Column('property_id', Integer, ForeignKey('properties.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    @classmethod
    def add_user(cls, username, password):
        if session.query(cls).filter_by(username=username).first():
            print(f"Користувач з іменем '{username}' вже існує.")
            return
        user = cls(username=username, password=password)
        session.add(user)
        session.commit()
        print(f"Додано користувача: {user}")

    @classmethod
    def authenticate(cls, username, password):
        user = session.query(cls).filter_by(username=username, password=password).first()
        return user is not None

    @classmethod
    def get_all_users(cls):
        return session.query(cls).all()

    @classmethod
    def delete_by_id(cls, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"Користувача з ID {user_id} видалено.")
        else:
            print(f"Користувача з ID {user_id} не знайдено.")

    @classmethod
    def update_by_id(cls, user_id, username=None, password=None):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            if username:
                user.username = username
            if password:
                user.password = password
            session.commit()
            print(f"Користувача з ID {user_id} оновлено.")
        else:
            print(f"Користувача з ID {user_id} не знайдено.")

    @classmethod
    def get_by_id(cls, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            return user
        else:
            print(f"Користувача з ID {user_id} не знайдено.")
            return None

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"


# Модель для категорій
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    thermometers = relationship("Thermometer", back_populates="category")

    @classmethod
    def add(cls, name):
        category = cls(name=name)
        session.add(category)
        session.commit()
        print(f"Додано категорію: {category}")

    @classmethod
    def update_by_id(cls, category_id, name=None):
        category = session.query(cls).filter_by(id=category_id).first()
        if category:
            if name:
                category.name = name
            session.commit()
            print(f"Категорію з ID {category_id} оновлено.")
        else:
            print(f"Категорію з ID {category_id} не знайдено.")

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def delete_by_id(cls, category_id):
        category = session.query(cls).filter_by(id=category_id).first()
        if category:
            session.delete(category)
            session.commit()
            print(f"Категорію з ID {category_id} видалено.")
        else:
            print(f"Категорію з ID {category_id} не знайдено.")

    @classmethod
    def get_by_id(cls, category_id):
        category = session.query(cls).filter_by(id=category_id).first()
        if category:
            return category
        else:
            print(f"Категорію з ID {category_id} не знайдено.")
            return None

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


# Модель для властивостей термометрів
class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    units = Column(String, nullable=False)

    thermometers = relationship("Thermometer", secondary=thermometer_property, back_populates="properties")

    @classmethod
    def add(cls, name, units):
        property_instance = cls(name=name, units=units)
        session.add(property_instance)
        session.commit()
        print(f"Додано властивість: {property_instance}")

    @classmethod
    def update_by_id(cls, property_id, name=None, units=None):
        property_instance = session.query(cls).filter_by(id=property_id).first()
        if property_instance:
            if name:
                property_instance.name = name
            if units:
                property_instance.units = units
            session.commit()
            print(f"Властивість з ID {property_id} оновлено.")
        else:
            print(f"Властивість з ID {property_id} не знайдено.")


    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def delete_by_id(cls, property_id):
        property_instance = session.query(cls).filter_by(id=property_id).first()
        if property_instance:
            session.delete(property_instance)
            session.commit()
            print(f"Властивість з ID {property_id} видалено.")
        else:
            print(f"Властивість з ID {property_id} не знайдено.")

    @classmethod
    def get_by_id(cls, property_id):
        property_instance = session.query(cls).filter_by(id=property_id).first()
        if property_instance:
            return property_instance
        else:
            print(f"Властивість з ID {property_id} не знайдено.")
            return None

    def __repr__(self):
        return f"Property(id={self.id}, name='{self.name}', units='{self.units}')"


# Модель для термометрів
class Thermometer(Base):
    __tablename__ = 'thermometers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    min_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)

    category = relationship("Category", back_populates="thermometers")
    properties = relationship("Property", secondary=thermometer_property, back_populates="thermometers")

    @classmethod
    def add(cls, name, vendor, category_name, min_temp, max_temp, accuracy, property_names):
        # Отримання категорії
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            print(f"Категорія '{category_name}' не знайдена")
            return

        # Отримання властивостей
        properties = session.query(Property).filter(Property.name.in_(property_names)).all()

        thermometer = cls(
            name=name, vendor=vendor, category=category,
            min_temp=min_temp, max_temp=max_temp, accuracy=accuracy,
            properties=properties
        )
        session.add(thermometer)
        session.commit()
        print(f"Додано термометр: {thermometer}")

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def delete_by_id(cls, thermometer_id):
        thermometer = session.query(cls).filter_by(id=thermometer_id).first()
        if thermometer:
            session.delete(thermometer)
            session.commit()
            print(f"Термометр з ID {thermometer_id} видалено.")
        else:
            print(f"Термометр з ID {thermometer_id} не знайдено.")

    @classmethod
    def update_by_id(cls, thermometer_id, name=None, vendor=None, category_id=None, min_temp=None, max_temp=None,
                     accuracy=None, property_ids=None):
        thermometer = session.query(cls).filter_by(id=thermometer_id).first()
        if thermometer:
            if name:
                thermometer.name = name
            if vendor:
                thermometer.vendor = vendor
            if category_id:
                thermometer.category_id = category_id
            if min_temp is not None:
                thermometer.min_temp = min_temp
            if max_temp is not None:
                thermometer.max_temp = max_temp
            if accuracy is not None:
                thermometer.accuracy = accuracy
            if property_ids:
                properties = session.query(Property).filter(Property.id.in_(property_ids)).all()
                thermometer.properties = properties
            session.commit()
            print(f"Термометр з ID {thermometer_id} оновлено.")
        else:
            print(f"Термометр з ID {thermometer_id} не знайдено.")

    @classmethod
    def get_by_id(cls, thermometer_id):
        thermometer = session.query(cls).filter_by(id=thermometer_id).first()
        if thermometer:
            return thermometer
        else:
            print(f"Термометр з ID {thermometer_id} не знайдено.")
            return None

    def __repr__(self):
        return (f"Thermometer(id={self.id}, name='{self.name}', vendor='{self.vendor}', "
                f"category='{self.category.name}', min_temp={self.min_temp}, max_temp={self.max_temp}, "
                f"accuracy={self.accuracy}, properties={[prop.name for prop in self.properties]})")


# Base.metadata.create_all(engine)

# Тестування

# Додавання користувачів
# User.add_user("admin", "password123")
# User.add_user("user1", "mypassword")
#
# # Перевірка автентифікації
# print("\nПеревірка автентифікації:")
# print("admin, password123 ->", User.authenticate("admin", "password123"))
# print("user1, wrongpassword ->", User.authenticate("user1", "wrongpassword"))
#
# # Додавання категорій
# Category.add("Електронні термометри")
# Category.add("Інфрачервоні термометри")
#
# # Додавання властивостей
# Property.add("Точність", "°C")
# Property.add("Діапазон температур", "°C")
#
# # Додавання термометрів із зв'язками
# Thermometer.add(
#     name="ThermoPro TP-50",
#     vendor="ThermoPro",
#     category_name="Електронні термометри",
#     min_temp=-50,
#     max_temp=70,
#     accuracy=0.1,
#     property_names=["Точність", "Діапазон температур"]
# )
#
# Thermometer.add(
#     name="Braun Thermoscan",
#     vendor="Braun",
#     category_name="Інфрачервоні термометри",
#     min_temp=-20,
#     max_temp=60,
#     accuracy=0.2,
#     property_names=["Точність"]
# )
#
# # Отримання всіх користувачів
# print("\nКористувачі:")
# for user in User.get_all_users():
#     print(user)
#
# # Отримання всіх категорій
# print("\nКатегорії:")
# for category in Category.get_all():
#     print(category)
#
# # Отримання всіх властивостей
# print("\nВластивості:")
# for property in Property.get_all():
#     print(property)
#
# # Отримання всіх термометрів
# print("\nТермометри:")
# for thermometer in Thermometer.get_all():
#     print(thermometer)