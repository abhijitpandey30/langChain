from langchain.vectorstores.chroma import Chroma;
from langchain_openai import OpenAIEmbeddings, ChatOpenAI;
from langchain.chains import RetrievalQA;
from dotenv import load_dotenv;
from redundant_filter_retriever import RedundantFilterRetriever
load_dotenv();


embeddings = OpenAIEmbeddings();
chat  =ChatOpenAI();



# This loads an existing Chroma database (if "emb" already exists).
# If you’re creating it for the first time, you’ll need to add documents before retrieval, but we already did it by running main.py once
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)

# retriever = db.as_retriever();

retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff" # 
)

result = chain.run("What is an interesting fact about English language");

print(result);

