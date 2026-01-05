from typing import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing import Annotated

class GraphState(TypedDict):
    question:str
    sql_query:str
    sql_result:str
    error:str | None

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]