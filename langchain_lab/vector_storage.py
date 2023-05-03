import langchain
from langchain.document_loaders import GitLoader
from langchain.vectorstores import FAISS
import os
from langchain.llms import OpenAI
import openai

#repo = 'https://github.com/EGAdams/monitored-object-js.git'

from git import Repo

repo = Repo.clone_from(
    #"https://github.com/hwchase17/langchain", to_path="./example_data/test_repo1"
    "https://github.com/EGAdams/monitored-object-js.git", to_path="./mb_data/test_repo1"
)
branch = repo.head.reference

# Create a GithubLoader instance
loader = GitLoader(repo_path="./mb_data/test_repo1", branch=branch )

# Load the entire repository
repo_contents = loader.load()


# Initialize LLM
with open(".env", "r") as f:
    key = f.read().strip()

print( "Key:", key )

os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(engine="ada")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

# Check if embeddings exist in local storage
if os.path.exists("embeddings.faiss"):
    # Load embeddings from local storage
    index = faiss.read_index("embeddings.faiss")
else:
    # Generate embeddings for data
    embeddings = []
    for file in data:
        embedding = llm.embed(file["page_content"])
        embeddings.append(embedding)
    embeddings = np.vstack(embeddings)

    # Store embeddings in local storage using FAISS
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    faiss.write_index(index, "embeddings.faiss")

# Use embeddings to find relevant data to include in prompt
D, I = index.search(query_embedding, k=5)
relevant_data = ""
for i in I[0]:
    relevant_data += data[i]["page_content"] + "\n"

# Generate new code with LLM
prompt = f"{relevant_data}\nCreate a monitored object that gets the time."
new_code = llm(prompt)


print ( len( embeddings ))
# Store the embeddings in Faiss
# index = faiss.IndexFlatL2( 512 )
# index.add( embeddings )
# faiss.write_index( index, './index.faiss' )

