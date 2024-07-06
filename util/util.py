import sys
import os
import regex as re

from dotenv import load_dotenv

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader

