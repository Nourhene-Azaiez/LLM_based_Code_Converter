# main.py
from utils.Chunker import *
from utils.CodeParser import *
import warnings
from utils.utils import *
from utils.Converter import *
from utils.Comparator import *

#Ignore the warning messages each time
warnings.filterwarnings("ignore", category=FutureWarning)

#--------------------------------------- Code folder ------------------------------------------------

# code_path="code_samples/p1.py"
code_path="code_samples/p2.py"

def detect_lan(code_path):
        if code_path.endswith('.py'):
            return "py"
        elif code_path.endswith('.java'):
            return "java"
        

with open(code_path, 'r') as file:
    code=file.read()

#--------------------------------------- Parse and Chunk Code ------------------------------------------------

parser = CodeParser([detect_lan(code_path)])
tree = parser.parse_code(code, detect_lan(code_path))
# points_of_interest = parser.extract_points_of_interest(tree, detect_lan(code_path))
grouped_nodes = parser.extract_points_of_interest_grouped(tree, "py")

#testing the output
for group in grouped_nodes:
    print("\n",group)

 
tokenlimit=calculate_mean_token_count(code)

chunker = CodeChunker(file_extension=detect_lan(code_path), encoding_name='gpt-4')
chunks = chunker.chunk(code, token_limit=tokenlimit)
CodeChunker.print_chunks(chunks)

#--------------------------------------- Convert Code ------------------------------------------------

# Initialize the CodeConverter class
converter = CodeConverter()

for chunk in chunks.values():
    # Define the code file path
    # code_path = "code_samples/p1.py"

    # Read the code from the file
    # with open(code_path, 'r') as file:
    #     code = file.read()

    # Generate the code conversion
    translation="""
    """
    score= 0.0
    attempt=1
    max_attempts=1
    while score < 0.5 and attempt <= max_attempts:
        attempt+=1
        result = converter.generate_text("python", "java", chunk)
        if "Report" in result:
            # Extract the code blocks from the generated report
            result=converter.code_extraction(result["Report"])
            comparator = CodeComparator(chunk, result, "java")
            scores = comparator.compare()
            score=scores["global_score"]
    translation+= result


#--------------------------------------- Compare Code ------------------------------------------------
comparator = CodeComparator(code, translation, "java")
print('----------------------------------')
print(translation)
print('----------------------------------')
print("Comparaison Scores:", scores)