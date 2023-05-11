import json
from pathlib import Path

from pprint import pprint

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from cache import Cache


try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


CACHE_DIR = Path(__file__).parent.parent / "data/cache"
CACHE_DIR.mkdir(exist_ok=True, parents=True)
CACHE_FILE = CACHE_DIR / "cache.json"

CHROMA_DATA_DIR = Path(__file__).parent.parent / "data/chroma"
if not CHROMA_DATA_DIR.exists():
    raise Exception(
        "Please run create_embeddings.py first to create the vectorstore. "
        "See README.md for more details."
    )


QUESTIONS = [
    "What perplexed Mr. McGregor when he returned to the garden?",
    "How did the cat manage to lock herself up inside the greenhouse?",
    "What did Peter do when he found a locked door in a wall?",
    "Who did Peter ask for directions to the gate?",
    "What did Peter see in the middle of the garden?",
    "What noise did Peter hear near the tool-shed?",
    "Who did old Mr. Benjamin Bunny cuffed off the basket and kicked into the greenhouse?",
    "Who did old Mr. Bunny take out of the garden with him?",
    "What did Peter do when he saw Mr. McGregor coming?",
    "What are the names of the characters in the stories?",
    "What's the name of a squirrel in the stories?",
    "What happened to the squirrel Nutkin?",
    "What happened to Peter?",
    "What's common between Peter and Benjamin?",
    "What happened to Benjamin?",
    "What was the story about mice?",
    "What were the names of the mice?",
    "What was the weather like in the stories?",
    "Could you extract all the names of the characters in all the stories?",
    "What animals are mentioned in the stories?",
]
# QUESTION = "What questions can I ask based on the texts?"
QUESTION = QUESTIONS[-1]

vectordb = Chroma(
    persist_directory=str(CHROMA_DATA_DIR), embedding_function=OpenAIEmbeddings()
)

chain = RetrievalQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
)


cache = Cache(CACHE_FILE)


def answer_question(question):
    if cached := cache.get(question):
        return cached
    res = chain({"question": question}, return_only_outputs=True)
    cache.set(question, res)
    return res


if __name__ == "__main__":
    pprint(answer_question(QUESTION))
