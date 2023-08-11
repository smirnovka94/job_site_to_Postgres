import psycopg2
from utils.DBPostgres import DBManager
from utils.func import printj, psycopg2_connect, create_bd, cook_db, fill_bd
from utils.hh_vacancies import HeadHunterAPI

if __name__ == '__main__':

    search_query = input("Введите Вакансию для поиска: ")

    # Запускаем поиск в HH.ru
    hh_api = HeadHunterAPI(search_query)
    # Получаем сокращенные данные по вакансиям из API сайта
    hh_vacancy = hh_api.short_data_vacancy()

    # Открываем pgAdmin
    password = input("Введите пароль от pgAdmin: ")

    conn = psycopg2_connect(password, "postgres")
    conn.autocommit = True
    cur = conn.cursor()
    db_name = "hh"
    try:
        cur.execute(f"DROP DATABASE {db_name}")
    except psycopg2.errors.InvalidCatalogName:
        pass
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()

    # Создаем Таблицы с Вакансиями и уникальными Компаниями
    create_bd(password, db_name)

    # Подготавливаем спарсенные данные с hh.ru для внедрения в таблицу
    data_vacancies, data_companies = cook_db(hh_vacancy)

    # Заполняем Таблицы готовыми данными
    fill_bd(password, db_name, data_vacancies, data_companies)

    # Запускаем DBManager
    postgres = DBManager(password)

    # postgres.get_companies_and_vacancies_count()

    # postgres.get_all_vacancies()

    # postgres.get_avg_salary()

    # postgres.get_vacancies_with_higher_salary()

    # postgres.get_vacancies_with_keyword()




