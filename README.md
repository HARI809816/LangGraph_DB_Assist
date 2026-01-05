# 🧠 AI-Powered SQL Database Assistant

An AI-driven database assistant that converts **natural language questions** into **safe, read-only PostgreSQL SQL queries** and executes them on a real database.  
This project demonstrates how **LLMs can safely interact with structured data** in production-style systems.

---

## 🚀 Features

- 🤖 Natural language → SQL generation using LLMs  
- 🔐 Strict **read-only SQL validation** (SELECT-only safety)  
- 🧬 Schema-aware prompting (reduces hallucinated tables/columns)  
- 🔗 Multi-table JOIN support  
- 📊 Handles analytical queries (aggregations, window functions, CTEs)  
- 🌐 Frontend → FastAPI → LLM → PostgreSQL flow  
- ⚙️ Modular backend design (LangGraph-ready)

---

## 🏗️ Architecture Overview

Frontend
↓
FastAPI API
↓
Prompt + LLM (LangGraph / LangChain)
↓
SQL Validation (Read-only)
↓
PostgreSQL Database
↓
Query Result


---

## 🛠️ Tech Stack

- **Backend**: FastAPI ⚡  
- **LLM Orchestration**: LangGraph / LangChain 🔗  
- **Database**: PostgreSQL 🐘  
- **DB Admin**: pgAdmin  
- **Package Manager**: uv 📦  
- **Language**: Python 🐍  

---

## 📦 Project Structure

langgraph-fastapi-db/
│
├── app/
│ ├── agent/ # SQL agent logic
│ ├── graph/ # LangGraph workflows
│ ├── llm/ # Prompt & LLM configuration
│ ├── db/ # Database connection & execution
│ └── utils/ # Validators, helpers
│
├── main.py # FastAPI entry point
├── README.md
└── pyproject.toml


---

## 🗄️ Supported Database (Example)

Designed and tested with a **real e-commerce schema**, including:

- users  
- products  
- categories  
- orders  
- order_items  
- payments  
- shipments  
- reviews  

The system can be adapted to **any PostgreSQL database**.

---

## 🔐 SQL Safety

To prevent destructive operations:

- Only `SELECT` queries are allowed  
- Keywords like `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE` are blocked  
- Unsupported questions return:

```sql
SELECT 'INSUFFICIENT_DATA';


## ▶️ Running the Project

Follow these steps to run the project locally.

---

### 1️⃣ Clone the Repository
 
git clone https://github.com/your-username/ai-sql-assistant.git
cd ai-sql-assistant


### 2️⃣ Create Virtual Environment (using uv)

uv venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate     # Windows

### 3️⃣ Install Dependencies

uv pip install -r requirements.txt

### 4️⃣ Set Environment Variables

DATABASE_URL=postgresql://username:password@localhost:5432/dbname
OPENAI_API_KEY=your_api_key_here


### 5️⃣ Run the Application

uvicorn main:app --reload
```
