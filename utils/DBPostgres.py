import psycopg2

from utils.func import psycopg2_connect, printdb


class DBManager():
    def __init__(self, password):
        self.password = password

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        self.conn = psycopg2_connect(self.password)
        cur = self.conn.cursor()
        cur.execute\
        ("""
        SELECT name_company, COUNT(vacancy.vacancy) FROM company
        INNER JOIN vacancy USING(id_company)
        GROUP BY name_company
        ORDER BY COUNT(vacancy.vacancy) DESC
        """)
        printdb(cur)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        self.conn = psycopg2_connect(self.password)
        cur = self.conn.cursor()
        cur.execute \
        ("""
        SELECT company.name_company, vacancy, salary, exchange, url  FROM vacancy
        INNER JOIN company USING(id_company)
        WHERE salary <> 0
        ORDER BY salary
        """)
        printdb(cur)
    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        self.conn = psycopg2_connect(self.password)
        cur = self.conn.cursor()
        cur.execute \
        ("""
        SELECT DISTINCT vacancy, COUNT(vacancy), ROUND(AVG(salary),0), exchange FROM vacancy
        WHERE salary <> 0
        GROUP BY vacancy, exchange
        ORDER BY ROUND(AVG(salary),0)
        """)
        printdb(cur)
    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.conn = psycopg2_connect(self.password)
        cur = self.conn.cursor()
        cur.execute \
            ("""
        SELECT vacancy, salary
        FROM vacancy
        WHERE salary > (SELECT 
        AVG(salary) 
        FROM vacancy
        )
        GROUP BY vacancy,salary
        ORDER BY salary
                """)
        printdb(cur)

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        self.conn = psycopg2_connect(self.password)
        cur = self.conn.cursor()
        cur.execute \
        ("""
        SELECT DISTINCT vacancy FROM vacancy
        WHERE vacancy LIKE '%python%' OR vacancy LIKE '%Python%'
        """)
        printdb(cur)
