import sqlite3
import pandas as pd

def run_analytics():
    print("=== ЭТАП 3.3: Аналитические SQL-запросы к базе данных ===")
    
    db_path = 'data/compliance.db'
    conn = sqlite3.connect(db_path)
    
    # -------------------------------------------------------------
    # ЗАПРОС 1: Собираем полный отчет по компаниям с "High Risk"
    # Здесь мы используем INNER JOIN, чтобы соединить таблицы по ключу company_id
    # -------------------------------------------------------------
    query_high_risk = """
    SELECT 
        c.company_name,
        c.hq_country,
        a.ai_risk_category,
        a.primary_trigger
    FROM companies c
    INNER JOIN ai_compliance a ON c.company_id = a.company_id
    WHERE a.ai_risk_category = 'High Risk';
    """
    
    print("\n[SQL Результат 1] Список компаний с ВЫСОКИМ УРОВНЕМ РИСКА (High Risk):")
    df_high_risk = pd.read_sql_query(query_high_risk, conn)
    print(df_high_risk)
    
    # -------------------------------------------------------------
    # ЗАПРОС 2: Считаем статистику — сколько компаний в каждой категории
    # Здесь мы используем агрегацию GROUP BY и сортировку ORDER BY
    # -------------------------------------------------------------
    query_stats = """
    SELECT 
        ai_risk_category AS "Категория риска",
        COUNT(company_id) AS "Количество компаний"
    FROM ai_compliance
    GROUP BY ai_risk_category
    ORDER BY "Количество компаний" DESC;
    """
    
    print("\n[SQL Результат 2] Сводная статистика по категориям закона EU AI Act:")
    df_stats = pd.read_sql_query(query_stats, conn)
    print(df_stats)
    
    conn.close()

if __name__ == "__main__":
    run_analytics()