import tiktoken
import json, logging
from utils.CodeParser import CodeParser

def count_tokens(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def load_json(json_file):
    with open(json_file) as f:
        return json.load(f)

import ast
import tokenize
from io import BytesIO

# Function to tokenize code and return the count of tokens
def count_tokens1(code):
    tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    return len([token for token in tokens if token.type != tokenize.ENCODING and token.type != tokenize.NEWLINE])

# Function to traverse the AST up to the second level of nesting
def analyze_structure(node, depth=0):
    if depth > 2:  # Only analyze up to the second depth
        return 0
    
    # If the node is a logical structure (function, class, etc.)
    token_count = 0
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        # Get the code inside the node and tokenize it
        code = ast.unparse(node)
        token_count += count_tokens1(code)
    
    # Recurse for child nodes (to handle nesting)
    for child in ast.iter_child_nodes(node):
        token_count += analyze_structure(child, depth + 1)
    
    return token_count

# Function to calculate the mean token count of logical structures
def calculate_mean_token_count(code: str, file_extension: str, parser: CodeParser) -> float:
    # Parse the code using tree-sitter
    tree_root = parser.parse_code(code, file_extension)  # Get the root node of the parsed tree
    if tree_root is None:
        logging.error(f"Failed to parse the code for {file_extension}")
        return 0.0
    
    total_tokens = 0
    structure_count = 1

    # Extract the structures of interest (functions, classes) based on the file extension
    points_of_interest = parser.extract_points_of_interest_grouped(tree_root, file_extension)

    for group in points_of_interest:
        for sub_group in group:
            for node, type_of_interest in sub_group:
                # Increment the structure count based on the type (e.g., 'Function', 'Class')
                if type_of_interest in ['Function', 'Class']:
                    structure_count += 1
                    # Add the size of the structure (i.e., number of tokens) to the total token count
                total_tokens += node.end_point[0] - node.start_point[0] + 1  # Calculate number of lines/tokens

    return total_tokens / structure_count
