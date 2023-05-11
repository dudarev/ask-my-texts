from pathlib import Path

import frontmatter

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# texts directory relative to this file directory
TEXTS_DIR = Path(__file__).parent.parent / "texts"
if not TEXTS_DIR.exists():
    raise Exception(
        "Please put your texts to be searched in a folder called 'texts' in the root of the project. "
        "See README.md for more details."
    )


CHROMA_DATA_DIR = Path(__file__).parent.parent / "data/chroma"
CHROMA_DATA_DIR.mkdir(exist_ok=True, parents=True)


texts = []
sources = []
for f in TEXTS_DIR.iterdir():
    with open(f) as fp:
        fm = frontmatter.load(fp)
        if title := fm.get("title"):
            print(f"Processing {title}")
            text_splitter = CharacterTextSplitter(
                chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
            )
            file_chunks = text_splitter.split_text(fm.content)
            file_sources = [
                f"{str(f.name).replace('.md','')}, chunk {i}"
                for i in range(len(file_chunks))
            ]
            texts.extend(file_chunks)
            sources.extend(file_sources)


embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_texts(
    texts,
    embeddings,
    metadatas=[{"source": source} for source in sources],
    persist_directory=str(CHROMA_DATA_DIR),
)
vectordb.persist()
