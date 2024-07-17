#!/usr/bin/env python

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
from langchain.chains import TransformChain

load_dotenv()

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create uppercase transform function
def uppercase_transform(inputs: dict) -> dict:
    return {"uppercase_text": inputs["text"].upper()}

uppercase_chain = TransformChain(
    input_variables=["text"],
    output_variables=["uppercase_text"],
    transform=uppercase_transform
)

# 5. Create chain
chain = prompt_template | model | parser | uppercase_chain

# 6. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 7. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)