from utils.Chunker import CodeChunker
from utils.CodeParser import CodeParser
from utils.Converter import CodeConverter
from utils.utils import calculate_mean_token_count
import warnings

# Ignore the warning messages each time
warnings.filterwarnings("ignore", category=FutureWarning)

class CodeConversionModule:
    def __init__(self, input_lang, output_lang):
        """
        Initialize the CodeConversionModule with input and output languages.
        
        :param input_lang: The input language ('py' for Python, 'java' for Java).
        :param output_lang: The output language ('py' for Python, 'java' for Java).
        """
        self.input_lang = input_lang
        self.output_lang = output_lang

    def convert_code(self, source_code):
        """
        Converts code from the input language to the output language.
        
        :param source_code: The code to be converted.
        :return: The converted code as a string.
        """
        # Parse and chunk the code
        parser = CodeParser([self.input_lang])
        tree = parser.parse_code(source_code, self.input_lang)
        grouped_nodes = parser.extract_points_of_interest_grouped(tree, self.input_lang)

        # Calculate token limit based on mean token count
        tokenlimit = calculate_mean_token_count(source_code)

        # Chunk the code based on token limit
        chunker = CodeChunker(file_extension=self.input_lang, encoding_name='gpt-4')
        chunks = chunker.chunk(source_code, token_limit=tokenlimit)

        # Initialize the CodeConverter class
        converter = CodeConverter()

        converted_code = ""
        for code in chunks.values():
            result = converter.generate_text(self.input_lang, self.output_lang, code)
            # Ensure 'Report' exists and is not None
            if "Report" in result and result["Report"]:
                extracted_code = converter.code_extraction(result["Report"])
                if extracted_code:  # Check if the extraction result is not None
                    converted_code += extracted_code

        return converted_code

