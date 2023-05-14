import os
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


is_openai_api_key_specified = os.environ.get("OPENAI_API_KEY")

if is_openai_api_key_specified:
    CHROMA_DATA_DIR = Path(__file__).parent.parent / "data/chroma"
    if not CHROMA_DATA_DIR.exists():
        raise Exception(
            "Please run create_embeddings.py first to create the vectorstore. "
            "See README.md for more details."
        )
    vectordb = Chroma(
        persist_directory=str(CHROMA_DATA_DIR), embedding_function=OpenAIEmbeddings()
    )
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
    )
else:
    vectordb = None
    chain = None


cache = Cache(CACHE_FILE)


def answer_question(question):
    if cached := cache.get(question):
        return cached
    if is_openai_api_key_specified:
        res = chain({"question": question}, return_only_outputs=True)
        cache.set(question, res)
    else:
        res = {
            "answer": "Please set OPENAI_API_KEY in your environment to get non-cached answers."
        }
    return res
