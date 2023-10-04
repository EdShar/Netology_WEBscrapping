import requests
import unicodedata
from bs4 import BeautifulSoup
import fake_headers
import json


def get_vacancies(html_data):
    html_soup = BeautifulSoup(html_data, 'lxml')
    vacancies_list = html_soup.find('main', class_='vacancy-serp-content')
    vacancies = vacancies_list.find_all('div', class_='serp-item')

    parsed_data = []

    for vacancy in vacancies:
        name = vacancy.find('a').text
        href = vacancy.find('a', class_='serp-item__title')['href']
        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        salary = vacancy.find('span', class_='bloko-header-section-2')

        if salary:
            salary = salary.text
        else:
            salary = 'Не указана'

        if open_vacancies(href):
            parsed_data.append({
                    "Вакансия": unicodedata.normalize('NFKD', name),
                    "Ссылка": href,
                    "Компания": unicodedata.normalize('NFKD', company),
                    "Город": unicodedata.normalize('NFKD', city),
                    "Зарплата": unicodedata.normalize('NFKD', salary)
            })

    return parsed_data


def open_vacancies(vacancy_url):
    response_vacancy = requests.get(url=vacancy_url, headers=headers.generate())
    vacancy_data = response_vacancy.text
    vacancy_soup = BeautifulSoup(vacancy_data, 'lxml')
    vacancies_desc = vacancy_soup.find(attrs={'data-qa':'vacancy-description'}).text

    if key[0] in vacancies_desc or key[1] in vacancies_desc:
        return True


def write_json(parsed_data):
    with open('final_vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, ensure_ascii=False)


if __name__ == '__main__':
    key = ['Django', 'Flask']

    headers = fake_headers.Headers(browser='chrome', os='win')

    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers.generate())
    main_data = response.text
    vacancies = get_vacancies(main_data)
    write_json(vacancies)
