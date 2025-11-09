from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler
from dotenv import load_dotenv;

load_dotenv();
handler = ChatModelStartHandler()
chat =ChatOpenAI(
    callbacks=[handler]
);

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# return_messages=True -> reuturn messages as list of messages rather than a bunch of  strings
tables = list_tables();

print(tables)
# prompt = ChatPromptTemplate.from_messages([
#     HumanMessagePromptTemplate.from_template("{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
    "You are an AI that has access to a SQLite database.\n"
    f"The database has tables: {tables}\n"
    "Do not make assumptions about what tables or columns exist. "
    "Instead, use the 'describe_tables' function when needed."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)
tools=[run_query_tool, describe_tables_tool, write_report_tool]
agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    # verbose=True,
    tools=tools,
    memory=memory
)

# agent_executor("How many users are in the database?")
# agent_executor.invoke({
#     "input": "How many users have provided shipping_address in the database?"
# })
# agent_executor.invoke({
#     "input": "Summarise the 5 most popular products. Write the report an HTML"
# })
agent_executor.invoke({
    "input": "How many orders are there?. Write the report an HTML"
})

# scratchpad is removed on second execution, we need to add memory
agent_executor.invoke({
    "input": "Repeat the same process of users"
})