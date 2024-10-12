import csv

with open('categories.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name'])
    writer.writerow([1, 'Електронні термометри'])
    writer.writerow([2, 'Інфрачервоні термометри'])

with open('properties.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'units'])
    writer.writerow([1, 'Точність', '°C'])
    writer.writerow([2, 'Діапазон температур', '°C'])

with open('thermometers.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'vendor', 'category', 'min_temp', 'max_temp', 'accuracy'])
    writer.writerow([1, 'ThermoPro TP-50', 'ThermoPro', 'Електронні термометри', -50, 70, 0.1])
    writer.writerow([2, 'Braun Thermoscan', 'Braun', 'Інфрачервоні термометри', -20, 60, 0.2])
