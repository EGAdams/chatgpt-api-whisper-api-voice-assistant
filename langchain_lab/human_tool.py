import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent

# get key from .env file
with open(".env", "r") as f:
    key = f.read().strip()

print( "Key:", key )

os.environ["OPENAI_API_KEY"] = key
openai.api_key = key
config.OPENAI_API_KEY

llm = ChatOpenAI(  temperature=0.0 )
math_llm = OpenAI( temperature=0.0 )

tools = load_tools( [ "human" ] )

agent_chain = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
)

agent_chain.run( "What is 555 - 5?" )
