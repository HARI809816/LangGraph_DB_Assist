from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import generate_sql,execute_sql,interpret_results

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("generate_sql_query", generate_sql)
    graph.add_node("execute_sql_query", execute_sql)
    graph.add_node("interpret_results", interpret_results)

    graph.set_entry_point("generate_sql_query")
    graph.add_edge("generate_sql_query", "execute_sql_query")
    graph.add_edge("execute_sql_query", "interpret_results")   
    graph.add_edge("interpret_results", END)

    return graph.compile()