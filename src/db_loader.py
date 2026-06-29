import pandas as pd
import sqlite3
import os

def load_data_to_sql():
    print("=== ЗАПУСК ПРОДВИНУТОГО ЗАГРУЗЧИКА В БАЗУ ДАННЫХ SQL ===")
    
    processed_file = 'data/processed_companies.csv'
    
    if not os.path.exists(processed_file):
        print(f"Ошибка: Файл {processed_file} не найден! Запустите сначала pipeline.py")
        return
        
    # Загружаем наши размеченные 239 компаний
    df = pd.read_csv(processed_file)
    print(f"Строк к загрузке: {len(df)}")
    
    # Подключаемся к базе eu_ai_act_monitor.db (которую использует app.py)
    conn = sqlite3.connect('eu_ai_act_monitor.db')
    cursor = conn.cursor()
    
    # Полностью очищаем старые таблицы, чтобы пересоздать их с правильной структурой
    cursor.execute("DROP TABLE IF EXISTS ai_compliance")
    
    print("Очистка завершена. Формируем две таблицы по схеме INNER JOIN...")
    
    # Шаг A: Создаем таблицу 'companies' в точном соответствии с запросом в app.py
    # Нам нужен уникальный ID для связки: company_id
    df['company_id'] = range(1, len(df) + 1)
    
    df_companies = pd.DataFrame({
        'company_id': df['company_id'],
        'company_name': df['company_name'],
        'hq_country': df['hq_country'],
        'industry': df['industry'],
        'description': df['description']
    })
    
    # Шаг B: Создаем таблицу 'ai_compliance'
    # Вычисляем колонку uses_ai: если риск минимальный — False (0), иначе True (1)
    uses_ai = df['risk_category'].apply(lambda x: 0 if x == 'Minimal Risk' else 1)
    
    # Определяем требуемое действие в зависимости от риска
    def get_action(risk):
        if risk == 'High Risk': return 'Strict Compliance & Audit Required'
        if risk == 'Specific Transparency Risk': return 'Labeling & Transparency Required'
        return 'No Action Required'
    
    required_actions = df['risk_category'].apply(get_action)
    
    df_compliance = pd.DataFrame({
        'company_id': df['company_id'],
        'uses_ai': uses_ai,
        'ai_risk_category': df['risk_category'],
        'primary_trigger': df['detected_triggers'],
        'required_action': required_actions,
        'confidence_score': df['confidence_score']
    })
    
    # Записываем обе таблицы в базу данных
    df_companies.to_sql('companies', conn, if_exists='replace', index=False)
    df_compliance.to_sql('ai_compliance', conn, if_exists='replace', index=False)
    
    # Финальная проверка работоспособности JOIN-запроса, на котором падал Streamlit
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM companies c 
            INNER JOIN ai_compliance a ON c.company_id = a.company_id
        """)
        rows_joined = cursor.fetchone()[0]
        print(f"\n=== УСПЕХ! Тестовый JOIN выполнен успешно. Связано строк: {rows_joined} ===")
    except Exception as e:
        print(f"\nОшибка при проверке запроса: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_data_to_sql()