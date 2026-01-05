from langchain_core.messages import HumanMessage, AIMessage
from .state import GraphState
from app.llm.sql_chain import llm  # Reuse LLM for interpretation

def generate_sql(state: GraphState):
    from app.llm.sql_chain import chain
    question = state["question"]
    
    state["messages"].append(HumanMessage(content=question))
    response = chain.invoke({"question": question})
    
    return {
        "sql_query": response.strip(),
        "messages": [AIMessage(content=f"🔍 SQL Generated:\n```\n{response}\n```")]
    }

def execute_sql(state: GraphState):
    from app.db.connection import db
    from sqlalchemy import text
    
    sql_query = state["sql_query"]
    
    try:
        with db.connect() as conn:
            result = conn.execute(text(sql_query)).fetchall()
        
        if result:
            result_str = str(result)[:1000]
            result_preview = f"Found {len(result)} rows:\n{result_str}"
        else:
            result_preview = "No matching results found"
        
        return {
            "sql_result": result_str,
            "error": None,
            "messages": [AIMessage(content=f"📊 Results:\n```\n{result_preview}\n```")]
        }
    except Exception as e:
        return {
            "sql_result": None,
            "error": str(e),
            "messages": [AIMessage(content=f"❌ SQL Error: {e}")]
        }

def interpret_results(state: GraphState):
    """Convert raw SQL results to human English"""
    question = state["question"]
    sql_result = state["sql_result"] or "No data"
    error = state["error"]
    
    if error:
        return {"messages": [AIMessage(content=f"**Final Answer**: {error}\nContact admin.")]}
    
    # LLM interprets results
    interpret_prompt = f"""
Question asked: {question}

Raw SQL results: {sql_result}

Convert to clear English answer. Be specific with numbers/dates. Keep concise.

Answer:
    """
    
    answer = llm.invoke(interpret_prompt).content.strip()
    
    return {
        "messages": [AIMessage(content=f"💬 **Answer**:\n{answer}")]
    }