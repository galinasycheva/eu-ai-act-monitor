# 🇪🇸 EU AI Act Monitor: Spain Tech Sector

An interactive Streamlit dashboard and analytical pipeline designed to assess Spanish startups and tech companies for compliance with the new European Artificial Intelligence regulation (**EU AI Act**).

The project automates data collection, risks classification based on company text descriptions, and stores the structured results in a relational database for subsequent monitoring.

---

## 🚀 Key Features
* **Data Extraction & Filtering:** Parsing and cleaning raw European startup data (isolated **239 target companies** located in Spain).
* **AI-Compliance Pipeline:** Automated text analysis of company descriptions based on regulatory risk triggers, categorizing them into risk levels (*High Risk*, *Specific Transparency Risk*, and *Minimal Risk*).
* **Relational Database Architecture:** Designing a structured SQLite database with distinct entities (tables `companies` and `ai_compliance`) connected via an `INNER JOIN` relationship using `company_id`.
* **Interactive Visualization:** A fully functional BI dashboard built with **Streamlit**, featuring dynamic metrics, risk distribution charts, and a smart full-text search registry.

---

## 🏗 Architecture & Data Flow

The project follows a standard ETL/Data Pipeline architecture:

1. `filter_spain.py` (Extract) — Extracts and filters the master dataset based on geographical location.
2. `pipeline.py` (Transform) — Analyzes descriptions, calculates a `confidence_score`, and assigns the appropriate risk category.
3. `db_loader.py` (Load) — Normalizes the structured data and loads it into two linked SQLite tables.
4. `app.py` (Visualize) — The Streamlit user interface that queries the SQLite database in real-time.

### Repository Structure:
```text
├── data/                  # Data directory (raw CSV and processed outputs)
├── src/
│   ├── filter_spain.py    # Geography filtering script
│   ├── pipeline.py        # Risk analysis scoring engine
│   ├── db_loader.py       # SQL database loader script
│   └── app.py             # Streamlit dashboard application
├── eu_ai_act_monitor.db   # SQLite database storage
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
## 🛠 Tech Stack
* **Core Language:** Python
* **Data Analysis:** Pandas, Openpyxl
* **Database Management:** SQLite3, SQL (INNER JOIN)
* **Dashboard / BI:** Streamlit

---

## 💻 How to Run Locally

1. Clone the repository:
```bash
git clone [https://github.com/galinasycheva/eu-ai-act-monitor.git](https://github.com/galinasycheva/eu-ai-act-monitor.git)
cd eu-ai-act-monitor
