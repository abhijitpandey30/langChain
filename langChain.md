# https://pdf.ai/
- more text-> more $ to run the request
- Break the entire text into chunks -> write an algo  to generate a summary of each chunk - this is done when user uploads a PDF
- When user asks a  question- > find he chunk that's most relevant + user's qustion and send it to chatGPT

# Embedding Creation Algo
- takes a string, and converts it into an array of numbers - all between 1 and -1
 - each number is a score of what the text talks about - [0.9, -.84] -> 0.9 for how happy the text is
 - An embedding is a special array of numbers that encodes what the chunk is talkig about
-1536 length of array
- We create embedding for each chunk, and store each embedding in a vector DB (Vector Stores)

- When user enters the a question-> we need to find the most relevant piece of text that represents that question-> create an embedding for that text -> take that embedding and find the most relevant chunk inside vector DB, use that + user Question-> get the most relevant answer from chatGPT
-> LANGCHAIN gives us tool to automate each of these steps

-> For e.g, it provides us classes to open up PDF and extract some text out of it
--> Githubissue loader, S3Loader, HTMLloader - basically classe to load data from anywhere!!


-> It even has classes that wrap implementation details for VECTOR dbs and make them simple to use
--> PGVector, Pinecone, Redis, Weaviate
--> TOOLS to automate EACH STEP OF A TEXT GENERATION PIPELINE!!
- EASY to swap LLM models, vector DBs while using almost same syntax



# CHAIN
-> INPUT to a -> PROMOT -> MODEL-> OUTPUT
 -  PROMPT template must declare the varibales tit needs to build the prompt

 - when we call llm=OpenAi()-> it looks for the OPENAI_API_KEY env variable