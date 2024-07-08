
# document-parser

`document-parser` is a tool designed to split a structured document into smaller chunks and export them as separate files. This process utilizes `regex` and `langchain`, an open-source framework that stores these chunks as embeddings (vector representations of the text) in a vector database. We use PineconeDB for our vector database. This tool is particularly useful for searching and retrieving information from large documents and has significant use-cases in GPT/LLM evaluations.

## How It Works

1. **Document Splitting**: The tool uses `regex` and ```langchain``` to parse and split the document into smaller chunks.
2. **Embedding and Storage**: The chunks are converted into vector representations using `langchain` and stored in PineconeDB.
3. **Query and Retrieval**:
    - A user submits a query.
    - The query is sent to the LLM to generate a vector representation.
    - This vector representation is used to perform a similarity search in the vector database.
    - Relevant chunks are retrieved from the vector database and fed into the LLM.
    - The LLM uses the initial query and the relevant chunks to generate a response.
    - The response is sent back to the user.


## Prerequisites
You **must** have an OpenAI API key, PineconeDB API key, and a PineconeDB index name to use this tool. You can sign up for a PineconeDB account [here](https://www.pinecone.io/). Please add these keys to your environment, the script expects them to be there as `PINECONE_API_KEY`, `OPENAI_API_KEY`, and `PINECONE_INDEX_NAME` respectively.

## Installation

To use `document-parser`, you need to have the following installed:

- Python 3.11 or higher
- Jupyter Notebook
- PineconeDB
- langchain
- Other dependencies listed in `requirements.txt`

### Follow the steps below to run document-parser:
1. **Clone the repository and enter it**:
    ```bash
    git clone https://github.com/umarhunter/document-parser.git
    cd document-parser
    ```

2. **Create a virtual environment using Conda**:
    ```bash
    conda create -n document-parser python=3.11.9
    ```
   
3. **Activate the virtual environment**:
    ```bash
   conda activate document-parser
    ```
   
4. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Optional: Run the Jupyter Notebook**:
    The Jupyter notebook (`document-parser.ipynb`) contains detailed notes on the underlying process.
    ```bash
    jupyter notebook document-parser.ipynb
    ```

4. **Run the script**:
    The script (`doc_parser.py`) can be executed with one parameter: the file path to the `.docx` file. Ensure the `.docx` file is located within the `docs/` directory and the file name does not contain spaces.
    ```bash
    python doc_parser.py --filename yourfile.docx
    ```
    This command will split `yourfile.docx` into smaller chunks, create vector embeddings for these chunks, and store them in PineconeDB.

## Notes

- Ensure your `.docx` files are placed in the `docs/` directory.
- The Jupyter notebook (`document-parser.ipynb`) provides detailed explanations and insights into each step of the process.
- The script should be run with file names that do not contain spaces for optimal performance.

## Contributing / Issues

Please feel free to contribute! If interested, fork the repository and submit a pull request with your changes. For any issues encountered, please feel free to submit them [here](https://github.com/umarhunter/document-parser/issues).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
