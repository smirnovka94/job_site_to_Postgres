import json
from configparser import ConfigParser

import psycopg2


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


def psycopg2_connect(password):
    """
    Подключается к БД
    :param password: Пароль от pgAdmin
    :return: connect
    """
    return psycopg2.connect(
            host = "localhost",
            database = "postgres",
            user="postgres",
            password=password,
            port=5432
            )

def create_bd(password):
    # Создаем Таблицы
    conn = psycopg2_connect(password)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                id_company INTEGER PRIMARY KEY,
                name_company VARCHAR(50) NOT NULL
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                id_vacancy INTEGER PRIMARY KEY,
                id_company serial,
                vacancy text,
                city VARCHAR,
                url VARCHAR(50),
                salary INTEGER,
                exchange VARCHAR(10),

                CONSTRAINT fk_company_vacancy FOREIGN KEY(id_company) REFERENCES company(id_company)
            )
        """)

    conn.commit()
    conn.close()

def cook_db(vacancy):
    # Ищем одинаковые названия компаний и генерируем словарь Название: условный номер
    data1, data2, data3, data4, data5, data6, data7 = vacancy
    data_vacancies = []
    dict_companies = {}
    for i, item in enumerate(data2):
        number = data2.index(item)
        dict_companies[item]=number
        # Создаем данные для таблицы вакансий
        db = (int(data1[i]), number, data3[i], data4[i], data5[i], int(data6[i]), data7[i])
        data_vacancies.append(db)

    # Создаем данные для таблицы компаний
    data_companies = []
    for key, values in dict_companies.items():
        db = (values, key)
        data_companies.append(db)

    return data_vacancies, data_companies

def fill_bd(password, vacancies, companies):
    conn = psycopg2_connect(password)

    # Заполняем данными Таблицу компаний
    with conn.cursor() as cur:
        cur.executemany("""
                        INSERT INTO company VALUES (%s, %s)""", companies)

    # Заполняем данными Таблицу вакансий
    with conn.cursor() as cur:
        cur.executemany("""
                INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s, %s)""", vacancies)
    conn.commit()
    conn.close()

def printdb(data):
    """
    Выгружает результат SQL запроса в консоль
    """
    rows = data.fetchall()
    for row in rows:
        print(row)