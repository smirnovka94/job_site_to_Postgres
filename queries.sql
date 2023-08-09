-- CREATE TABLES
CREATE TABLE company
(
    id_company INTEGER PRIMARY KEY,
    name_company VARCHAR(50) NOT NULL
);

CREATE TABLE vacancy
(
	id_vacancy INTEGER PRIMARY KEY,
	id_company serial,
	vacancy text,
	city VARCHAR,
	url VARCHAR(50),
	salary INTEGER,
	exchange VARCHAR(10),

	CONSTRAINT fk_company_vacancy FOREIGN KEY(id_company) REFERENCES company(id_company)
);


-- получает список всех компаний и количество вакансий у каждой компании

SELECT name_company, COUNT(vacancy.vacancy) FROM company
INNER JOIN vacancy USING(id_company)
GROUP BY name_company
ORDER BY COUNT(vacancy.vacancy) DESC;

-- получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT company.name_company, vacancy, salary, exchange, url  FROM vacancy
INNER JOIN company USING(id_company)
WHERE salary <> 0
ORDER BY salary;

-- получает среднюю зарплату по вакансиям.
SELECT DISTINCT vacancy, COUNT(vacancy), ROUND(AVG(salary),0), exchange FROM vacancy
WHERE salary <> 0
GROUP BY vacancy, exchange
ORDER BY ROUND(AVG(salary),0);

-- получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT vacancy, salary
FROM vacancy
WHERE salary > (
	SELECT
	AVG(salary)
	FROM vacancy
				)
GROUP BY vacancy,salary
ORDER BY salary;

-- получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
SELECT DISTINCT vacancy FROM vacancy
WHERE vacancy LIKE '%python%' OR vacancy LIKE '%Python%';