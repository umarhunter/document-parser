import argparse
from util.util import *
import sys
import os
import regex as re
import yaml
from dotenv import load_dotenv
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader


def main(path):
    if path is not None:
        assert path.endswith('.docx'), 'File must be a Word document (.docx)'
    else:
        raise ValueError("No file path provided.")

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

    pc = Pinecone(api_key=PINECONE_API_KEY)
    embeddings = OpenAIEmbeddings()

    filepath = "./docs/" + path
    loader = Docx2txtLoader(filepath)
    data = loader.load()

    # the string containing keywords and definitions
    page_content = data[0].page_content

    # regex that'll match a keyword followed by a colon and a definition
    pattern = r"(?<=^|\n)([\w\s/()]+?):\s*(.*?)(?=\n[\w\s/()]+?:|\Z)"

    # find all matches of the pattern in the page_content string
    matches = re.findall(pattern, page_content, re.DOTALL)

    # Convert matches to a dictionary
    keywords_definitions = {keyword.strip(): definition.strip() for keyword, definition in matches}

    # Open a new .txt file in write mode
    with open('keywords_definitions.txt', 'w') as file:
        # Iterate through the keywords_definitions dictionary
        for keyword, definition in keywords_definitions.items():
            # Write the keyword and its definition to the file
            file.write(f"{keyword}: {definition}\n\n")

    file_path = 'keywords_definitions.txt'
    keywords_definitions = read_keywords_from_file(file_path)

    for keyword, definition in keywords_definitions.items():
        filename = sanitize_filename(keyword) + '.yaml'
        filename = "./results/" + filename
        with open(filename, 'w') as file:
            yaml.dump({keyword: definition}, file, default_flow_style=False)

    loader = TextLoader("keywords_definitions.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    vectorstore_from_texts = PineconeVectorStore.from_documents(
        docs,
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )


    vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    #vectorstore.similarity_search(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gather file name')
    parser.add_argument('--filename', type=str, help='Name of the Word (.docx) document to be parsed')
    args = parser.parse_args()
    main(args.path)
