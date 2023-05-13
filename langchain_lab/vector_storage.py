# Step 1: Install required packages (if not already installed)
# !pip install faiss-cpu
# !pip install langchain
# Import additional required libraries
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chat_models.openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
import numpy as np
from typing import List
from langchain.document_loaders import GitLoader
from langchain.vectorstores import FAISS
import os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from git import Repo

repo = Repo.clone_from( "https://github.com/egadams/monitored-object-js.git", to_path="./mb_data/test_repo1" )

branch = repo.head.reference

# Create a GithubLoader instance
loader = GitLoader(repo_path="./mb_data/test_repo1", branch=branch)

# Initialize LLM
with open( ".env", "r" ) as f:
    key = f.read().strip()

print( "Key:", key)

os.environ["OPENAI_API_KEY"] = key
llm = OpenAI( engine="ada", api_key=key )

data = loader.load()

print( "Splitting documents in chunks ..." )
chunk_size = 8000
chunk_overlap = 3000
doc_splitter = CharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
docs = doc_splitter.split_documents(data)

print( "Building the vector database ..." )

embeddings = OpenAIEmbeddings( openai_api_key=key )

print( "populating docsearch ..." )
#problem is after here...
docsearch = Chroma.from_documents(docs, embeddings)

print( "Building the retrieval chain ..." )
finalChain = RetrievalQAWithSourcesChain.from_chain_type(
    ChatOpenAI(),
    chain_type="map_reduce",
    retriever=finalChain.as_retriever(),
)

print( "Knowledge base created!" )
