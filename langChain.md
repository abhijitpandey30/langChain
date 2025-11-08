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

 #LLM 
 - Large Langugae Models
 - Traditional LLM-> completion style
 - https://platform.openai.com/chat/edit?models=gpt-4.1
 --> just add to the last message

 Conversationsal styles - back and forth messaging -> ChatGPT, Bard, Claude
 -> most legacy ones are completion

 # FileChatMessageHistory - > we are able to save all our messages so that we can show it, just like chatgpt stores it on the left
 -> right now we are storing it in file, but we can store it also in redis, mysql etc
 - this might be expensive, since we are keeping on adding messages, and this increases the token size we send to OpenAi servers.
 - ConversationSummaryMemory, on the other hand, has it's own promt and llm, it creates a summary of our system, user and ai message, and creates a syste message for the next question
 - # The memory is used twice per chain call — once before the model runs, and once after.

-Specifically:

# Before the LLM is called → the chain loads memory (to inject past messages into the prompt).

# After the LLM returns → the chain saves the new interaction (user input + model output) back into memory.

 - use verbose=True to see those messages

 - langchain also has loader to load u files rom s3 -> 

 - longer the prompt, more time and more money to run

 # A vector Store is. database that is specialised in storing/seacrhing around these emeddings
 -> ChromaDB -> open souce -> internally uses SQLlite
 -> langChain has it's own wrapper for ChromaDB