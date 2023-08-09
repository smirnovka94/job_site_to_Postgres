import requests
import json


class HeadHunterAPI():
    def __init__(self, name):
        self.name = name


    def get_vacancies(self):
        # Отправляем GET-запрос на API для получения списка вакансий
        params = {
            'text': self.name,
            'per_page': 100,  # Количество вакансий для отображения (максимум 100)
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)

        # Если запрос успешен, получаем данные вакансий в формате JSON
        if response.status_code == 200:
            vacancies_data = response.json()

            # Возвращаем список вакансий
            return vacancies_data['items']

        else:
            # Если запрос не удался, выводим сообщение об ошибке
            print('Не удалось получить данные вакансий')
            return []

    @property
    def id_s(self):
        id_s = [values['id'] for values in self.get_vacancies()]
        return id_s

    @property
    def company_s(self):
        company_s = [values['employer']['name'] for values in self.get_vacancies()]
        return company_s
    @property
    def name_s(self):
        name_s = [values['name'] for values in self.get_vacancies()]
        return name_s
    @property
    def city_s(self):
        city_s = [values['area']['name'] for values in self.get_vacancies()]
        return city_s
    @property
    def url_s(self):
        url_s =[values['alternate_url'] for values in self.get_vacancies()]
        return url_s
    @property
    def salary_s(self):
        """
        Ищет указания Заработной платы
        :return: 0, при None
        :return: Зарплату 'до' , если Зарплата 'от' не указана
        :return: Зарплату 'от' , во всех остальных случаях
        """
        salary_s = []
        for values in self.get_vacancies():
            if values['salary'] == None:
                salary_s.append(0)
                continue
            elif values['salary']['from'] == None:
                salary_s.append(int(values['salary']['to']))
            else:
                salary_s.append(int(values['salary']['from']))
        return salary_s

    @property
    def exchange_s(self):
        exchange_s = []
        for values in self.get_vacancies():
            if values['salary'] == None:
                exchange_s.append('')
            else:
                exchange_s.append(values['salary']['currency'])
        # exchange_s = [values['salary']['currency'] for values in self.get_vacancies()]
        return exchange_s

    def short_data_vacancy(self):
        return self.id_s, self.company_s, self.name_s, self.city_s, self.url_s, self.salary_s , self.exchange_s

