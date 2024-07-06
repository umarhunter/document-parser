import argparse
#from util.util import *
import sys
import os
import regex as re

from dotenv import load_dotenv

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

    # Example usage: print each keyword and its definition
    for keyword, definition in keywords_definitions.items():
        print(f"{keyword}: {definition}\n")

    # Open a new .txt file in write mode
    with open('keywords_definitions.txt', 'w') as file:
        # Iterate through the keywords_definitions dictionary
        for keyword, definition in keywords_definitions.items():
            # Write the keyword and its definition to the file
            file.write(f"{keyword}: {definition}\n\n")

    file_path = 'keywords_definitions.txt'
    keywords_definitions = read_keywords_from_file(file_path)
    print(keywords_definitions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gather file names and ')
    parser.add_argument('--path', type=str, help='File path to a Word (.docx) document')
    args = parser.parse_args()
    main(args.path)
