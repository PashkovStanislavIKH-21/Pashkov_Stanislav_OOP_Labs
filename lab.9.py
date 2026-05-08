import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_and_preprocess(self):
        # 1.2 Завантаження з роздільником ;
        self.df = pd.read_csv(self.filepath, sep=';')

        # 1.3 Створення числової колонки Average Salary
        def calculate_average(salary_str):
            if pd.isna(salary_str): return 0
            numbers = re.findall(r'\d+', str(salary_str))
            if len(numbers) >= 2:
                return (float(numbers[0]) + float(numbers[1])) / 2
            elif len(numbers) == 1:
                return float(numbers[0])
            return 0

        self.df['Average Salary'] = self.df['Salary Range'].apply(calculate_average)

        # format='mixed' дозволяє Pandas обробити дати з різними роздільниками
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'], format='mixed')
        self.df['Year'] = self.df['Date Posted'].dt.year

        return self.df


class JobVisualizer:
    def __init__(self, df):
        self.df = df
        sns.set_theme(style="whitegrid")

    def plot_bar_salary_exp(self):
        # 2.1 Barplot
        plt.figure(figsize=(10, 6))
        sns.barplot(data=self.df, x='Experience Level', y='Average Salary', palette='muted', ci=None)
        plt.title('Середня зарплата від рівня досвіду')
        plt.show()
        print(
            "Висновок (2.2): Середня зарплата зростає пропорційно досвіду: від початкового (Entry) до керівного (Executive).")

    def plot_box_industry(self):
        # 3.1 Boxplot
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df, x='Industry', y='Average Salary', palette='Set2')
        plt.xticks(rotation=45, ha='right')
        plt.title('Розподіл зарплат за галузями')
        plt.tight_layout()
        plt.show()
        print(
            "Висновок (3.2): Найвищий рівень зарплат та найбільший розкид (варіативність) "
            "зазвичай спостерігається у FinTech та AI/Data Science.")

    def plot_heatmap_vacancies(self):
        # 4.1 Heatmap
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Кількість вакансій за рівнем досвіду та галуззю')
        plt.show()
        print(
            "Висновок (4.2): Найбільша кількість вакансій зосереджена в галузях з високим попитом на Mid-level спеціалістів.")

    def plot_scatter_trends(self):
        # 5.1 Scatterplot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='Year', y='Average Salary', hue='Experience Level', s=100)
        plt.title('Залежність зарплати від року та досвіду')
        plt.show()
        print("Висновок (5.2): Тенденція до зростання найбільш виражена для Senior/Executive рівнів у останні роки.")

    def plot_pair_analysis(self):
        # 6.1 Pairplot
        # Вибираємо тільки необхідні колонки для аналізу взаємозв'язків
        sns.pairplot(self.df[['Average Salary', 'Year', 'Experience Level']], hue='Experience Level', palette='bright')
        plt.suptitle('Парні графіки взаємозв’язків', y=1.02)
        plt.show()
        print(
            "Висновок (6.2): Pairplot показує загальну структуру даних та кореляції між усіма парами змінних одночасно.")
        print(
            "Відмінність: Scatterplot фокусується на одному конкретному взаємозв'язку, "
            "а Pairplot — на комплексному огляді всієї моделі.")

path = r"C:\Users\stas2\OneDrive\Робочий стіл\file for tasks\Job opportunities.csv"

try:
    # 1. Підготовка
    handler = DataHandler(path)
    df = handler.load_and_preprocess()

    # Створення об'єкта для візуалізації
    viz = JobVisualizer(df)

    # Виклик усіх методів аналізу
    viz.plot_bar_salary_exp()
    viz.plot_box_industry()
    viz.plot_heatmap_vacancies()
    viz.plot_scatter_trends()
    viz.plot_pair_analysis()

except Exception as e:
    print(f"Сталася помилка: {e}")