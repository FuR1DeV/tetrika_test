import json
import requests
from random import randint
from bs4 import BeautifulSoup

"""
В этом задании я немножко усложнил задачу, добавив словарь со всеми животными,
записав их в json файл, а так же создал генератор случайных имен.
"""


def parse_animals():

    # Создаем парсер для создания полного списка животных взятых из Wikipedia
    url = f"https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    page = 0
    animal_list = []
    print("Надо немножко подождать")
    while page != 97:
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "lxml")
        main_page = soup.find_all("div", class_="mw-category mw-category-columns")
        for i in main_page:
            name = i.find_all("li")
            for v in name:
                animal_list.append(v.find("a").get("title"))
        new_url = soup.find_all(attrs={"title": "Категория:Животные по алфавиту"})[1].get('href')
        url = f"https://ru.wikipedia.org{new_url}"
        page += 1
        if page == 50:
            print("Уже готово на половину")
    return animal_list


def count_animals(animal_list):

    # Создаем нужные переменные для нашего вычисления
    count, res_json, occurrences_count, res_animal_list = 0, {}, {}, []
    alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К',
                'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
                'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']

    # Вычисляем
    while count <= len(alphabet) - 1:
        for animal in animal_list:
            if alphabet[count] == animal[0]:
                res_animal_list.append(animal)
        res_json[f'{alphabet[count]} - {len(res_animal_list)}'] = res_animal_list.copy()
        occurrences_count[f'{alphabet[count]}'] = len(res_animal_list)
        res_animal_list.clear()
        count += 1

    # Запишем результат полного вычисления в словарь
    with open("res.json", "w", encoding='utf-8') as file:
        json.dump(res_json, file, indent=4, ensure_ascii=False)

    # Выводим полученные данные в консоль в соответствии с ТЗ
    for i in occurrences_count:
        print(f"{i}: {occurrences_count[i]}")


# Генератор случайных имен как в ТЗ
def random_name_generator():
    with open('res.json', 'r', encoding='utf-8') as file:
        a = json.load(file)
        rand_key = randint(0, 28)
        key = list(a)[rand_key]
        rand_value = randint(0, len(a[key]))
        print(f"Ваше случайное имя - {a[key][rand_value]} {rand_value}")
    file.close()


def main():
    count_animals(parse_animals())
    random_name_generator()


if __name__ == '__main__':
    main()
