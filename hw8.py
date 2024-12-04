import pandas as pd
import numpy as np
from scipy import stats

# Загрузка данных
url = 'https://raw.githubusercontent.com/obulygin/pyda_homeworks/master/statistics_basics/horse_data.csv'
data = pd.read_csv(url, header=None, na_values='?')

# Переименуем столбцы для удобства анализа (по описанию данных в .names)
columns = [
    'surgery', 'age', 'hospital_number', 'rectal_temp', 'pulse', 'respiratory_rate',
    'temperature_extremities', 'peripheral_pulse', 'mucous_membrane', 'capillary_refill_time',
    'pain', 'peristalsis', 'abdominal_distention', 'nasogastric_tube', 'nasogastric_reflux',
    'nasogastric_reflux_ph', 'rectal_exam_feces', 'abdomen', 'packed_cell_volume',
    'total_protein', 'abdom_appearance', 'abdom_total_protein', 'outcome', 'surgical_lesion',
    'lesion_1', 'lesion_2', 'lesion_3', 'cp_data'
]
data.columns = columns

# Выбор столбцов для анализа: выбраны 4 числовых и 4 категориальных
selected_columns = ['rectal_temp', 'pulse', 'respiratory_rate', 'packed_cell_volume',
                    'surgery', 'age', 'pain', 'outcome']
df = data[selected_columns]

# Задание 1: Базовое изучение (расчет метрик)
# Для числовых данных
numerical_columns = ['rectal_temp', 'pulse', 'respiratory_rate', 'packed_cell_volume']
for col in numerical_columns:
    print(f'Столбец: {col}')
    print(f'Среднее: {df[col].mean()}')
    print(f'Медиана: {df[col].median()}')
    print(f'Мода: {df[col].mode()[0]}')
    print(f'Стандартное отклонение: {df[col].std()}')
    print(f'Минимум: {df[col].min()}')
    print(f'Максимум: {df[col].max()}')
    print()

# Для категориальных данных
categorical_columns = ['surgery', 'age', 'pain', 'outcome']
for col in categorical_columns:
    print(f'Столбец: {col}')
    print(f'Мода: {df[col].mode()[0]}')
    print(f'Частота уникальных значений:\n{df[col].value_counts()}')
    print()

# Задание 2: Поиск выбросов в числовых столбцах
for col in numerical_columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f'Выбросы в столбце {col}: {len(outliers)}')
    print(f'Границы выбросов: нижняя {lower_bound}, верхняя {upper_bound}')
    print()

# Принятие решения о работе с выбросами
# В данном случае выбросы можно либо удалить, либо заменить, в зависимости от дальнейшего анализа.
df = df[(df['rectal_temp'] >= lower_bound) & (df['rectal_temp'] <= upper_bound)]
# Можно продолжить для остальных столбцов аналогично, например, удалить или заменить выбросы.

# Задание 3: Работа с пропусками
# Подсчёт пропусков в каждом из выбранных столбцов
missing_values = df.isnull().sum()
print("Количество пропусков в каждом столбце:\n", missing_values)

# Заполнение пропусков
# Числовые столбцы: заполняем средним или медианой
for col in numerical_columns:
    df[col] = df[col].fillna(df[col].median())  # Заполняем пропуски медианой

# Категориальные столбцы: заполняем наиболее частым значением (модой)
for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])  # Заполняем пропуски модой

# Проверка отсутствия пропусков
print("Проверка отсутствия пропусков:\n", df.isnull().sum())

# Итоговый dataframe без пропусков
print(df.head())