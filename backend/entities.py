import csv
import json
import xml.etree.ElementTree as ET


# Базовий клас для списків
class BaseList:
    def __init__(self):
        self.dataArray = []
        self.index = 0

    def delete(self, id):
        self.dataArray = [item for item in self.dataArray if item.get_id() != id]

    def display_all(self):
        for item in self.dataArray:
            print(item.display_info())

    def save_to_csv(self, filename):
        raise NotImplementedError("This method should be implemented in child classes")


# Клас для категорій
class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def edit(self, name):
        self.name = name

    def display_info(self):
        return f"{self.id}. {self.name}\n"


class CategoryList(BaseList):
    def __init__(self):
        super().__init__()
        self.load_from_csv("categories.csv")

    def add(self, name):
        self.index += 1
        new_category = Category(self.index, name)
        self.dataArray.append(new_category)
        return self.index

    def edit(self, id, name):
        for item in self.dataArray:
            if item.get_id() == id:
                item.edit(name)

    def load_from_csv(self, filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = Category(int(row["id"]), row["name"])
                self.dataArray.append(category)

    def save_to_csv(self, filename="categories.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name"])
            for category in self.dataArray:
                writer.writerow([category.get_id(), category.name])


# Клас для властивостей
class Property:
    def __init__(self, id, name, units):
        self.id = id
        self.name = name
        self.units = units

    def get_id(self):
        return self.id

    def edit(self, name, units):
        self.name = name
        self.units = units

    def display_info(self):
        return f"{self.id}. {self.name} ({self.units})\n"


class PropertyList(BaseList):
    def __init__(self):
        super().__init__()
        self.load_from_csv("properties.csv")

    def add(self, name, units):
        self.index += 1
        new_property = Property(self.index, name, units)
        self.dataArray.append(new_property)
        return self.index

    def edit(self, id, name, units):
        for item in self.dataArray:
            if item.get_id() == id:
                item.edit(name, units)

    def load_from_csv(self, filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                property = Property(int(row["id"]), row["name"], row["units"])
                self.dataArray.append(property)

    def save_to_csv(self, filename="properties.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "units"])
            for property in self.dataArray:
                writer.writerow([property.get_id(), property.name, property.units])


# Клас для термометрів
class Thermometer:
    def __init__(self, id, name, vendor, category, min_temp, max_temp, accuracy, properties):
        self.id = id
        self.name = name
        self.vendor = vendor
        self.category = category
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.accuracy = accuracy
        self.properties = properties

    def get_id(self):
        return self.id

    def edit(self, name, vendor, category, min_temp, max_temp, accuracy, properties):
        self.name = name
        self.vendor = vendor
        self.category = category
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.accuracy = accuracy
        self.properties = properties

    def display_properties(self):
        result = 'Характеристики:\n'
        for key, value in self.properties.items():
            result += f"{key}: {value}\n"
        return result

    def display_info(self):
        return (f"{self.id}. {self.vendor} {self.name}\n"
                f"Категорія: {self.category}\n"
                f"Температурний діапазон: від {self.min_temp} до {self.max_temp}\n"
                f"Точність: {self.accuracy}\n" + self.display_properties())


class ThermometerList(BaseList):
    def __init__(self):
        super().__init__()
        self.load_from_csv("thermometers.csv")

    def add(self, name, vendor, category, min_temp, max_temp, accuracy, properties):
        self.index += 1
        new_thermometer = Thermometer(self.index, name, vendor, category, min_temp, max_temp, accuracy, properties)
        self.dataArray.append(new_thermometer)
        return self.index

    def edit(self, id, name, vendor, category, min_temp, max_temp, accuracy, properties):
        for item in self.dataArray:
            if item.get_id() == id:
                item.edit(name, vendor, category, min_temp, max_temp, accuracy, properties)

    def load_from_csv(self, filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                properties = {"Точність": row["accuracy"], "Діапазон температур": f'{row["min_temp"]} до {row["max_temp"]}°C'}
                thermometer = Thermometer(int(row["id"]), row["name"], row["vendor"], row["category"], row["min_temp"], row["max_temp"], row["accuracy"], properties)
                self.dataArray.append(thermometer)

    def save_to_csv(self, filename="thermometers.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "vendor", "category", "min_temp", "max_temp", "accuracy"])
            for thermometer in self.dataArray:
                writer.writerow([thermometer.get_id(), thermometer.name, thermometer.vendor, thermometer.category, thermometer.min_temp, thermometer.max_temp, thermometer.accuracy])


# Тестування програми
category_list = CategoryList()
property_list = PropertyList()
thermo_list = ThermometerList()

# Виведення даних
category_list.display_all()
print("\n")
property_list.display_all()
print("\n")
thermo_list.display_all()

# Збереження змін до CSV
category_list.save_to_csv()
property_list.save_to_csv()
thermo_list.save_to_csv()
