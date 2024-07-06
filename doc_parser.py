import argparse
from util.util import *

def main(path):
    if path is not None:
        assert path.endswith('.docx'), 'File must be a Word document (.docx)'
    else:
        raise ValueError("No file path provided.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gather file names and ')
    parser.add_argument('--path', type=str, help='File path to a Word (.docx) document')
    args = parser.parse_args()
    main(args.path)
