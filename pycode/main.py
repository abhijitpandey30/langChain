from langchain_openai import OpenAI;
from langchain.prompts import PromptTemplate;
from langchain.chains import LLMChain, SequentialChain;
import argparse;
from dotenv import load_dotenv;

load_dotenv();

parser = argparse.ArgumentParser();
parser.add_argument("--task", default="return a list of numbers");
parser.add_argument("--language", default="python")
args = parser.parse_args();

#   SECURE THIS KEY!
# api_key = "DUMMY KEY"

# llm = OpenAI(openai_api_key=api_key);
llm = OpenAI();

code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"]
)
test_prompt = PromptTemplate(
    template="Write a test for the following {language} code:\n {code}",
    input_variables=["language", "code"]
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code"
)
test_chain= LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="test"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["task", "language"],
    output_variables=["code", "test"]
)

# result = llm.invoke("Write a very very short poem");
result = chain({
    "language":args.language,
    "task": args.task
})


print(">>>>> GENERATED CODE:");
print(result["code"]);

print(">>>> GENERATED test");
print(result["test"])

