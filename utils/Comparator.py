import os
import ast
import subprocess
from bert_score import score

class CodeComparator:
    def __init__(self, source_code, translated_code,source_description,target_description, source_language="Python"):
        self.source_code = source_code
        self.translated_code = translated_code
        self.source_language = source_language
        self.source_description=source_description
        self.target_description=target_description

    @staticmethod
    def validate_python_syntax(code):
        """
        Validate Python syntax using the AST parser.
        """
        try:
            ast.parse(code)
            return 1
        except SyntaxError:
            return 0

    @staticmethod
    def validate_java_syntax(code):
        """
        Validate Java syntax using the `javac` command.
        """
        try:
            class_name = CodeComparator.extract_class_name(code)
            file_name = f"{class_name}.java"
            with open(file_name, "w") as f:
                f.write(code)
            result = subprocess.run(["javac", file_name], capture_output=True, text=True)
            return 1 if result.returncode == 0 else 0
        finally:
            # Cleanup temporary file
            if os.path.exists(file_name):
                os.remove(file_name)

    @staticmethod
    def validate_javascript_syntax(code):
        try:
            result = subprocess.run(["node", "-c", "-e", code], capture_output=True, text=True)
            return 1 if result.returncode == 0 else 0
        except Exception:
            return 0

    @staticmethod
    def validate_typescript_syntax(code):
        try:
            file_name = "temp.ts"
            with open(file_name, "w") as f:
                f.write(code)
            result = subprocess.run(["tsc", "--noEmit", file_name], capture_output=True, text=True)
            return 1 if result.returncode == 0 else 0
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

    @staticmethod
    def validate_css_syntax(code):
        try:
            from cssutils import parseString
            parseString(code)
            return 1
        except Exception:
            return 0
    
    @staticmethod
    def validate_php_syntax(code):
        try:
            file_name = "temp.php"
            with open(file_name, "w") as f:
                f.write(code)
            result = subprocess.run(["php", "-l", file_name], capture_output=True, text=True)
            return 1 if "No syntax errors detected" in result.stdout else 0
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

    @staticmethod
    def validate_ruby_syntax(code):
        try:
            result = subprocess.run(["ruby", "-c", "-e", code], capture_output=True, text=True)
            return 1 if "Syntax OK" in result.stdout else 0
        except Exception:
            return 0

    @staticmethod
    def extract_class_name(code):
        """
        Extract the public class name from Java code.
        """
        for line in code.splitlines():
            if line.strip().startswith("public class"):
                return line.split()[2]
        return "Main"

    @staticmethod
    def compute_bertscore(reference, candidate):
        """
        Compute BERTScore for the reference and candidate code.
        """
        P, R, F1 = score([candidate], [reference], lang='en')
        return F1.mean().item()

    @staticmethod
    def compute_composite_score(source_syntax_score, translate_syntax_score, similarity_score, 
                                source_syntax_weight=0.1, translate_syntax_weight=0.3, similarity_weight=0.6):
        """
        Compute a composite score by combining individual scores with weights.
        """
        return (
            (source_syntax_score * source_syntax_weight) +
            (translate_syntax_score * translate_syntax_weight) +
            (similarity_score * similarity_weight)
        )

    def compare(self):
        """
        Compare source and translated code, returning the composite score.
        """
        if self.source_language.lower() == "python":
            source_syntax_score = self.validate_python_syntax(self.source_code)
            translate_syntax_score = self.validate_java_syntax(self.translated_code)
        else:
            source_syntax_score = self.validate_java_syntax(self.source_code)
            translate_syntax_score = self.validate_python_syntax(self.translated_code)

        # Use BLEU or BERTScore for similarity
        similarity_score = self.compute_bertscore(self.source_description, self.target_description)

        composite_score = self.compute_composite_score(
            source_syntax_score, translate_syntax_score, similarity_score
        )

        return {
            "source_syntax_score": source_syntax_score,
            "translate_syntax_score": translate_syntax_score,
            "similarity_score": similarity_score,
            "global_score": composite_score
        }

