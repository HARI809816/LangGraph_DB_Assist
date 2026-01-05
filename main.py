from fastapi import FastAPI
from app.graph.workflow import build_graph
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

@app.get("/ask")
async def ask(question: str):
    result = graph.invoke({"question": question, "messages": []})
    #print(result)
    
    # Clean response
    final_answer = result["messages"][-1].content
    return {
        "question": question,
        "sql_result": result["sql_result"],
        "answer": final_answer,
        "sql_query": result["sql_query"],
        "row_count": len(result["sql_result"] or []),
        "success": result["error"] is None
    }


def main():
    print("Hello from langgraph-fastapi-db!")


if __name__ == "__main__":
    main()
 