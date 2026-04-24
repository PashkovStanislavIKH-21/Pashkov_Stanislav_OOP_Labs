import pandas as pd


class DataManager:

    @staticmethod
    def load_data(file_path):

        df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')
        df.index = df.index + 1
        return df

    @staticmethod
    def basic_info(df):
        print("--- Перші 5 рядків ---")
        print(df.head())
        print("\n--- Останні 5 рядків ---")
        print(df.tail())
        print(f"\nРозмірність: {df.shape[0]} рядків, {df.shape[1]} стовпців")
        print(f"Обсяг пам'яті: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")


class DataAnalyzer:

    @staticmethod
    def check_quality(df):
        print("\n--- Типи даних ---")
        print(df.dtypes)
        print("\n--- Пропущені значення ---")
        missing = df.isnull().sum()
        print(missing)
        if missing.sum() == 0:
            print("\nВисновок: Дані чисті, пропуски відсутні.")
        else:
            print(f"\nВисновок: Знайдено {missing.sum()} пропущених значень.")


class JobFilter:

    @staticmethod
    def analyze_salary(df):
        # Витягуємо числа з текстового діапазону
        df['Min Salary'] = df['Salary Range'].str.extract(r'(\d+)').astype(float)
        df['Max Salary'] = df['Salary Range'].str.extract(r'-(\d+)').astype(float)

        top_5 = df.sort_values(by='Max Salary', ascending=False).head(5)
        return top_5


class Statistics:

    @staticmethod
    def industry_stats(df):
        stats = df.groupby('Industry').agg(
            Count=('Job Title', 'count'),
            Avg_Min_Salary=('Min Salary', 'mean')
        )
        top_industry = stats['Avg_Min_Salary'].idxmax()
        return stats, top_industry

    @staticmethod
    def create_categories(df):
        def categorize(max_sal):
            if max_sal <= 40000:
                return 'Low'
            elif max_sal <= 70000:
                return 'Medium'
            else:
                return 'High'

        df['Salary Category'] = df['Max Salary'].apply(categorize)
        return df


class TimeSeriesAnalysis:

    @staticmethod
    def analyze_by_year(df):
        df['Date Posted'] = pd.to_datetime(df['Date Posted'])
        df['Year'] = df['Date Posted'].dt.year
        yearly_activity = df.groupby('Year').agg(Job_Count=('Job Title', 'count'))
        return yearly_activity


file_path = r'C:\Users\stas2\OneDrive\Робочий стіл\file for lab.3\Job opportunities.csv'

try:
    # 1. Імпорт
    df = DataManager.load_data(file_path)
    DataManager.basic_info(df)

    # 2. Аналіз структури
    DataAnalyzer.check_quality(df)

    # 3 & 4. Фільтрація та аналіз зарплат
    top_jobs = JobFilter.analyze_salary(df)
    print("\n--- Топ-5 найбільш високооплачуваних вакансій ---")
    print(top_jobs[['Job Title', 'Salary Range', 'Max Salary']])

    # 5. Групування
    ind_stats, best_ind = Statistics.industry_stats(df)
    print("\n--- Статистика за галузями ---")
    print(ind_stats)
    print(f"\nГалузь з найвищою середньою зарплатою: {best_ind}")

    # 6. Використання apply()
    df = Statistics.create_categories(df)
    print("\n--- Перевірка категорій зарплат (перші 5) ---")
    print(df[['Job Title', 'Max Salary', 'Salary Category']].head())

    # 7. Часовий аналіз
    yearly = TimeSeriesAnalysis.analyze_by_year(df)
    print("\n--- Кількість вакансій за роками ---")
    print(yearly)

    print("\nВИСНОВОК: Аналіз завершено успішно.")

except FileNotFoundError:
    print(f"ПОМИЛКА: Файл не знайдено за шляхом: {file_path}")
    print("Перевірте, чи правильно вказано ім'я користувача.")
except Exception as e:
    print(f"Виникла помилка: {e}")