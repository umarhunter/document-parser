import sys
import os
import regex as re

from dotenv import load_dotenv

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader


def read_keywords_from_file(file_path):
    keywords_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:  # Ensure the line contains a colon
                keyword, definition = line.split(':', 1)  # Split on the first colon only
                keywords_dict[keyword.strip()] = definition.strip()
    return keywords_dict


def sanitize_filename(filename):
    """Sanitize the string to make it a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)[:255]
