import sqlite3
import pandas as pd
import re


class DatabaseManager:

    def __init__(self, db_name='it_jobs.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def load_csv_to_sqlite(self, csv_file, table_name='jobs'):
        # Завантажуємо дані, пропускаючи проблемні рядки
        df = pd.read_csv(csv_file, sep=';', on_bad_lines='skip')

        # Видаляємо зайві пробіли з назв стовпців
        df.columns = df.columns.str.strip()

        if 'Salary Range' not in df.columns:
            print("ПОМИЛКА: Стовпець 'Salary Range' не знайдено!")
            return

        # Попередня обробка Salary Range
        def parse_salary(salary_str):
            if pd.isna(salary_str): return 0
            nums = re.findall(r'\d+', str(salary_str).replace(',', ''))
            nums = [int(n) for n in nums]
            return sum(nums) / len(nums) if nums else 0

        df['avg_salary'] = df['Salary Range'].apply(parse_salary)
        df['max_salary'] = df['Salary Range'].apply(
            lambda x: max([int(n) for n in re.findall(r'\d+', str(x).replace(',', ''))] or [0]))

        df.index = df.index + 1

        df.to_sql(table_name, self.conn, if_exists='replace', index=True, index_label='ID')
        print(f"Дані успішно завантажені в таблицю '{table_name}'.")

    def execute_query(self, query):
        df = pd.read_sql_query(query, self.conn)
        df.index = df.index + 1  # Зміщуємо індекс для гарного виводу
        return df

    def close(self):
        self.conn.close()
        print("З'єднання з БД закрито.")


class JobAnalytics:

    def __init__(self, db_manager):
        self.db = db_manager

    def basic_queries(self):
        print("\n--- Перші 10 вакансій ---")
        print(self.db.execute_query("SELECT * FROM jobs LIMIT 10"))

        print("\n--- Вакансії з вимогою SQL ---")
        query = "SELECT * FROM jobs WHERE `Required Skills` LIKE '%SQL%'"
        print(self.db.execute_query(query))

        print("\n--- Унікальні локації та компанії ---")
        print(self.db.execute_query("SELECT DISTINCT Location, Company FROM jobs"))

    def financial_analytics(self):
        print("\n--- Середня зарплата за рівнем досвіду ---")
        print(self.db.execute_query(
            "SELECT `Experience Level`, AVG(avg_salary) as AvgSalary FROM jobs GROUP BY `Experience Level`"))

        print("\n--- Кількість вакансій за рівнем досвіду ---")
        print(
            self.db.execute_query("SELECT `Experience Level`, COUNT(*) as Count FROM jobs GROUP BY `Experience Level`"))

        print("\n--- Мін/Мак зарплата серед усіх вакансій ---")
        print(self.db.execute_query("SELECT MIN(avg_salary) as MinSalary, MAX(avg_salary) as MaxSalary FROM jobs"))

    def industry_analytics(self):
        print("\n--- Кількість вакансій в індустріях (ЗП > 50,000) ---")
        print(self.db.execute_query("SELECT Industry, COUNT(*) FROM jobs WHERE avg_salary > 50000 GROUP BY Industry"))

        print("\n--- Складний звіт: Локація + Досвід ---")
        query = """
            SELECT Location, `Experience Level`, COUNT(*) as Count, AVG(avg_salary) as AvgSalary 
            FROM jobs 
            GROUP BY Location, `Experience Level`
        """
        print(self.db.execute_query(query))

    def advanced_practice(self):
        print("\n--- Топ 5 вакансій за максимальною зарплатою ---")
        print(self.db.execute_query("SELECT * FROM jobs ORDER BY max_salary DESC LIMIT 5"))

        print("\n--- Найактивніші компанії 2023 року ---")
        print(self.db.execute_query("""
            SELECT Company, COUNT(*) as Vacancies 
            FROM jobs 
            WHERE Year = 2023 
            GROUP BY Company 
            ORDER BY Vacancies DESC 
            LIMIT 5
        """))


# --- Виконання ---

# 1. Підготовка (Завдання 1)
db = DatabaseManager('it_jobs_market.db')

file_path = r'C:\Users\stas2\OneDrive\Робочий стіл\file for lab.3\Job opportunities.csv'

try:
    db.load_csv_to_sqlite(file_path)

    # 2. Аналітика (прибираємо решітки, щоб методи запрацювали)
    analytics = JobAnalytics(db)
    analytics.basic_queries()
    analytics.financial_analytics()
    analytics.industry_analytics()
    analytics.advanced_practice()

except Exception as e:
    print(f"Помилка при виконанні: {e}")

finally:
    # 3. Закриття з'єднання (виконається завжди)
    db.close()