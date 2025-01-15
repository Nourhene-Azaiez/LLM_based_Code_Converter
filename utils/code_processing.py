import warnings
from utils.Chunker import CodeChunker
from utils.CodeParser import CodeParser
from utils.utils import calculate_mean_token_count
from utils.Converter import CodeConverter
from utils.Comparator import CodeComparator


class CodeProcessor:
    def __init__(self, code_path):
        self.code_path = code_path
        self.language = self.detect_language(code_path)
        self.code = self.read_code()
        self.parser = CodeParser([self.language])
        warnings.filterwarnings("ignore", category=FutureWarning)

    @staticmethod
    def detect_language(code_path):
        if code_path.endswith('.py'):
            return "py"
        elif code_path.endswith('.java'):
            return "java"
        else:
            raise ValueError("Unsupported file type. Only .py and .java are supported.")

    def read_code(self):
        with open(self.code_path, 'r') as file:
            return file.read()

    def parse_and_chunk(self):
        # Parse the code
        tree = self.parser.parse_code(self.code, self.language)
        grouped_nodes = self.parser.extract_points_of_interest_grouped(tree, self.language)
        
        # Print groups for debugging (optional)
        for group in grouped_nodes:
            print("\n", group)

        # Calculate token limit and chunk the code
        token_limit = calculate_mean_token_count(self.code)
        chunker = CodeChunker(file_extension=self.language, encoding_name='gpt-4')
        chunks = chunker.chunk(self.code, token_limit=token_limit)
        CodeChunker.print_chunks(chunks)

        return chunks

    def convert_code(self, chunks, target_language="java"):
        converter = CodeConverter()
        translation = ""
        for chunk in chunks.values():
            score = 0.0
            attempt = 1
            max_attempts = 1

            while score < 0.5 and attempt <= max_attempts:
                attempt += 1
                result = converter.generate_text(self.language, target_language, chunk)
                
                if "Report" in result:
                    # Extract code from the report
                    result = converter.code_extraction(result["Report"])

                    # Ensure result is a string before appending
                    if isinstance(result, str):
                        translation += result
                    else:
                        # Handle cases where the result is not a string
                        translation += str(result)  # Convert result to a string if necessary
                    
                    # Compare the code
                    comparator = CodeComparator(chunk, result, target_language)
                    scores = comparator.compare()
                    score = scores["global_score"]

        return translation   # Return both the translation and the scores

    def compare_code(self, translation, target_language="java"):
        comparator = CodeComparator(self.code, translation, target_language)
        scores = comparator.compare()
        return scores


def process_code(file_path):
    processor = CodeProcessor(file_path)

    # Parse and chunk code
    chunks = processor.parse_and_chunk()

    # Convert code
    translation = processor.convert_code(chunks)

    # Compare code
    scores = processor.compare_code(translation)

    return translation, scores
