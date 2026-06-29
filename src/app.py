import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="EU AI Act Monitor - Spain", layout="wide")

# Функция загрузки данных из ПРАВИЛЬНОЙ базы данных
def load_data_from_correct_db():
    db_path = 'eu_ai_act_monitor.db'
    
    if not os.path.exists(db_path):
        st.error(f"База данных {db_path} не найдена! Проверьте путь.")
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    
    # Объединяем базовую инфо о компаниях (таблица c) и разметку рисков (таблица a)
    query = """
    SELECT 
        c.company_name, 
        c.hq_country, 
        c.industry, 
        c.description, 
        a.uses_ai, 
        a.ai_risk_category, 
        a.primary_trigger, 
        a.required_action, 
        a.confidence_score 
    FROM companies c 
    INNER JOIN ai_compliance a ON c.company_id = a.company_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🇪🇸 EU AI Act Monitor: Spain Tech Sector")
st.subheader("Анализ соответствия испанских стартапов требованиям регуляции ИИ")

# Загружаем данные
df = load_data_from_correct_db()

if not df.empty:
    # Главные метрики сверху
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего компаний в базе", len(df))
    with col2:
        # ИСПРАВЛЕНО: используем 'ai_risk_category' вместо 'risk_category'
        high_risk_count = len(df[df['ai_risk_category'] == 'High Risk'])
        st.metric("High Risk (Высокий риск)", high_risk_count)
    with col3:
        # ИСПРАВЛЕНО: используем 'ai_risk_category' вместо 'risk_category'
        transparency_count = len(df[df['ai_risk_category'] == 'Specific Transparency Risk'])
        st.metric("Specific Transparency Risk", transparency_count)

    st.markdown("---")

    # График распределения рисков
    st.write("### Распределение компаний по категориям риска:")
    # ИСПРАВЛЕНО: считаем по правильной колонке
    risk_counts = df['ai_risk_category'].value_counts()
    st.bar_chart(risk_counts)

    st.markdown("---")

    # Интерактивная таблица с поиском
    st.write("### Реестр компаний и триггеры рисков")
    search_query = st.text_input("Поиск по названию компании или описанию:")
    
    if search_query:
        df_filtered = df[
            df['company_name'].str.contains(search_query, case=False, na=False) |
            df['description'].str.contains(search_query, case=False, na=False)
        ]
    else:
        df_filtered = df

    # ИСПРАВЛЕНО: выводим именно те колонки, которые создал db_loader.py
    # ('ai_risk_category', 'primary_trigger', 'confidence_score')
    columns_to_show = ['company_name', 'industry', 'ai_risk_category', 'primary_trigger', 'confidence_score', 'description']
    
    # Проверяем, что все колонки есть в наличии, чтобы избежать новых KeyError
    available_columns = [col for col in columns_to_show if col in df_filtered.columns]
    
    st.dataframe(
        df_filtered[available_columns],
        use_container_width=True
    )
else:
    st.warning("База данных пуста или не загрузилась.")