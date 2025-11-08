from langchain.document_loaders import TextLoader;
from langchain.text_splitter import CharacterTextSplitter;
from langchain.embeddings import OpenAIEmbeddings;
from langchain.vectorstores.chroma import Chroma;
from dotenv import load_dotenv;
import langchain
langchain.debug = True
load_dotenv();

embeddigs = OpenAIEmbeddings();

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200, # It will find the first 200 char, then find the nearest \n, so chunk size maybe be greater than 200 characters
    chunk_overlap=0 # should be more for Pdfs
)

loader = TextLoader("facts.txt");

docs = loader.load_and_split(text_splitter=text_splitter);

# This is running eveytime we run our program, storing duplicate embeddings, 
# so when we searh, we will start seeing duplicate results
db = Chroma.from_documents(
    docs, # A chroma instance is created, reach out OpenAi embeddings and create embeddings for each doc
    embedding=embeddigs,
    persist_directory="emb"
)

# here CHROMAdb is helping us with finding the most reevent embeddings with our questions, we can do the same with a retrival chain
results = db.similarity_search_with_score(
    "What is an interesting fact about English language",
    k=2 # by default it returns top 4
) 

for doc, score in results:
    print("\n---")
    print(f"Score: {score:.4f}")
    print(f"Content: {doc.page_content}")
    

# for doc in docs:
#     print(doc.page_content)