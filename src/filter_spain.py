import pandas as pd

# 1. Загружаем исходный файл EXCEL
try:
    # Используем read_excel вместо read_csv
    df_eu = pd.read_excel('data/EU-Startups Database.xlsx')
    print(f"Загружено {len(df_eu)} строк из европейской базы данных Excel.")
except Exception as e:
    print(f"Ошибка при чтении Excel-файла: {e}")
    print("Подсказка: Проверьте, что файл лежит в папке data и называется точно 'EU-Startups Database.xlsx'")
    exit()

# 2. Фильтруем по столбцу Category1, где упоминается Spain
df_spain = df_eu[df_eu['Category1'].str.contains('Spain', case=False, na=False)].copy()

print(f"Успешно отфильтровано! Найдено компаний в Испании: {len(df_spain)}")

# 3. Приводим таблицы к нашему стандарту колонок
df_ready = pd.DataFrame({
    'company_name': df_spain['Title'],
    'hq_country': 'Spain',
    'industry': df_spain['Category1'],
    'description': df_spain['Description']
})

# Убираем строки, если описание пустое
df_ready = df_ready.dropna(subset=['description'])

# 4. Сохраняем в наш рабочий raw_companies.csv
df_ready.to_csv('data/raw_companies.csv', index=False)
print("Файл data/raw_companies.csv успешно создан и заполнен испанскими компаниями!")