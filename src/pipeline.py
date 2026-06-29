import pandas as pd

def analyze_compliance_mock(description: str) -> dict:
    # Приводим к нижнему регистру для надежности поиска
    desc_lower = str(description).lower()
    
    # 1. Высокий риск (ИИ в HR, найме, биометрии, оценке людей, скоринге)
    if any(word in desc_lower for word in ['hr', 'recruitment', 'hiring', 'cv', 'scoring', 'credit', 'evaluation']):
        return {
            "risk_category": "High Risk",
            "confidence_score": 0.95,
            "detected_triggers": "Automated human/financial evaluation or HR systems"
        }
    
    # 2. Риск прозрачности (Генеративный ИИ, чат-боты, распознавание лиц/голоса, ML)
    elif any(word in desc_lower for word in ['ai', 'machine learning', 'deep learning', 'vision', 'nlp', 'chatbot', 'generative']):
        return {
            "risk_category": "Specific Transparency Risk",
            "confidence_score": 0.90,
            "detected_triggers": "AI/ML tech stack or generative models detected"
        }
    
    # 3. Минимальный риск (ВСЕ ОСТАЛЬНЫЕ КОМПАНИИ — софт, дизайн, маркетинг без ИИ)
    else:
        return {
            "risk_category": "Minimal Risk",
            "confidence_score": 0.85,
            "detected_triggers": "Standard software, web development, or traditional SaaS"
        }

def run_pipeline():
    print("=== ЗАПУСК ПАЙПЛАЙНА РАЗМЕТКИ РИСКОВ ===")
    
    # Читаем наши 239 испанских компаний
    df = pd.read_csv('data/raw_companies.csv')
    print(f"Загружено из raw_companies.csv: {len(df)} строк.")
    
    # Списки для сбора результатов
    risk_categories = []
    confidence_scores = []
    triggers = []
    
    # Пробегаем по каждой строчке БЕЗ исключения
    for idx, row in df.iterrows():
        result = analyze_compliance_mock(row['description'])
        
        risk_categories.append(result['risk_category'])
        confidence_scores.append(result['confidence_score'])
        triggers.append(result['detected_triggers'])
        
    # Добавляем новые колонки в наш DataFrame
    df['risk_category'] = risk_categories
    df['confidence_score'] = confidence_scores
    df['detected_triggers'] = triggers
    
    # ВНИМАНИЕ: Сохраняем результат в ОТДЕЛЬНЫЙ файл processed_companies.csv,
    # чтобы никогда не портить исходный raw_companies.csv!
    df.to_csv('data/processed_companies.csv', index=False)
    print(f"Успешно обработано и сохранено в processed_companies.csv: {len(df)} строк.")

if __name__ == "__main__":
    run_pipeline()