import  pandas as pd

# Чтение файла и его преобразование в список
db = pd.read_csv('pseudo-db.csv')
dblist = db.values.tolist()

# Функция для фильтрации списка по городу и возрасту
def filter_data(city, min_age, max_age):
    filtered_data = [person for person in dblist if person[1] == city and min_age <= person[2] <= max_age]
    return filtered_data

# Функция для фильтрации списка по возрасту
def filter_data_without_city(min_age, max_age):
    filtered_data = [person for person in dblist if min_age <= person[2] <= max_age]
    return filtered_data