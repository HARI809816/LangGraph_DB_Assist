from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.db.connection import db
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from datetime import datetime, timedelta

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

sql_db = SQLDatabase(db)



def get_dynamic_info():
    """Dynamic schema + dates"""
    tables = sql_db.get_usable_table_names()
    schema_parts = []
    for table in tables:
        info = sql_db.get_table_info([table])
        schema_parts.append(f"**{table}**: {info}")
    
    # DYNAMIC DATES
    now = datetime.now()
    last_month = now - timedelta(days=30)
    yesterday = now - timedelta(days=1)
    
    date_info = f"""
CURRENT DATE INFO:
- Today: {now.strftime('%Y-%m-%d')}
- Last 30 days: >= '{last_month.strftime('%Y-%m-%d')}'
- Yesterday: '{yesterday.strftime('%Y-%m-%d')}'
Use: WHERE created_at >= 'YYYY-MM-DD'
    """
    
    return "\n\n".join(schema_parts) + "\n\n" + date_info

SCHEMA_AND_DATES = get_dynamic_info()
print("✅ Schema + Dates loaded!")


SQL_PROMPT = f"""
You are an expert PostgreSQL SQL Query generator for an e-commerce system.

First Think : 
    Understand the user's question and break it down how to make as query for the database.
        

TASK:
Convert the user's natural language question into a VALID, READ-ONLY PostgreSQL SQL query.

STRICT RULES:
- Use ONLY the tables and columns provided in the SCHEMA
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE
- Do NOT explain the query
- Do NOT use markdown formatting
- Output ONLY the SQL query

SCHEMA:
{SCHEMA_AND_DATES}

TEXT SEARCH:
- Products by name: WHERE name ILIKE '%headphones%'
- Categories: WHERE name ILIKE '%bluetooth%'
- Users: WHERE name ILIKE '%John%'

ADVANCED SQL GUIDANCE:
- Use CTEs (WITH clauses) when solving multi-step problems
- Use window functions (SUM() OVER, ROW_NUMBER, RANK) when required
- For percentage or contribution analysis, compute totals and cumulative values
- Sort before applying cumulative calculations
- Prefer deterministic ordering

Examples :
    📋 LOOKUP QUERIES:
    Q: Kurt price → SELECT p.price, p.name FROM products p JOIN users u ON ... WHERE u.name ILIKE '%kurt%';
    Q: iPhone price → SELECT AVG(price) FROM products WHERE name ILIKE '%iphone%';
    Q: Electronics → SELECT * FROM products WHERE category='Electronics';

    👥 USER QUERIES:
    Q: Kurt orders → SELECT o.* FROM orders o JOIN users u ON o.user_id=u.id WHERE u.name ILIKE '%kurt%';
    Q: Active users → SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id=o.user_id GROUP BY u.id HAVING COUNT(o.id)>0;

    💰 REVENUE ANALYTICS:
    Q: Top products → SELECT p.name, SUM(oi.quantity*oi.unit_price) FROM products p JOIN order_items oi ON p.id=oi.product_id GROUP BY p.id ORDER BY 2 DESC LIMIT 5;
    Q: 80% revenue → WITH ranked AS (... ORDER BY revenue DESC), total AS (...) SELECT * FROM ranked WHERE SUM(revenue) OVER(ORDER BY revenue DESC) <= total.total * 0.8;
    Q: Monthly revenue → SELECT DATE_TRUNC('month', o.created_at), SUM(o.total) FROM orders o GROUP BY 1 ORDER BY 1;

    📊 ADVANCED:
    Q: Customer LTV → SELECT u.name, SUM(o.total) FROM users u JOIN orders o ON u.id=o.user_id GROUP BY u.id ORDER BY 2 DESC;
    Q: Repeat buyers → SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id GROUP BY u.id HAVING COUNT(o.id) > 1;

    TEXT SEARCH: ILIKE '%kurt%', '%iphone%', '%headphones%'
    DATES: created_at >= 'YYYY-MM-DD', DATE_TRUNC('month', created_at)

RELATIONSHIP ASSUMPTIONS:
users → orders → order_items → products

FAIL-SAFE:
- If the question cannot be answered using the schema, return exactly:
  SELECT 'INSUFFICIENT_DATA';

QUESTION:
{{question}}

SQL QUERY:
"""




prompt = ChatPromptTemplate.from_template(SQL_PROMPT)
chain = prompt | llm | StrOutputParser()