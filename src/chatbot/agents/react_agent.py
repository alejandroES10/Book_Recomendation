from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from ollama.ollama_llm import llm
from chatbot.tools.tool_for_search_books import tool_for_search_book
from langchain_core.messages import AIMessage, HumanMessage



memory = MemorySaver()
agent_executor = create_react_agent(llm, tools=[tool_for_search_book], checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

for s in agent_executor.stream(
    {"messages": [HumanMessage(content="Hola me llamo Ale")]}, config=config
):
    print(s)
    print("----")