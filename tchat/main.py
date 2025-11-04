from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# Initialize the model
chat = ChatOpenAI(verbose=True)

# Create memory (stores previous conversation turns)
memory = ConversationSummaryMemory(
    # chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages", 
    return_messages=True,  # we are working with chat-based memory
    llm=chat
)

# Create prompt template (system remembers messages + current input)
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="messages"), 
    HumanMessagePromptTemplate.from_template("{content}")
])

# Chain together model, prompt, and memory
chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

# Interactive chat loop
while True:
    content = input(">> ")
    result = chain.run(content=content)
    print(result)
