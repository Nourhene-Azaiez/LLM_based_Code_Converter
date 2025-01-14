import subprocess
import ast
import difflib
import os


# Function to validate Python syntax
def validate_python_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# Function to validate Java syntax
def validate_java_syntax(code):
    with open("Main.java", "w") as temp_file:
        temp_file.write(code)
    result = subprocess.run(["javac", "Main.java"], capture_output=True)
    return result.returncode == 0


# Function to execute Python code and return True if no errors
def execute_python_code(code):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return True  # Execute successfully
    except Exception as e:
        return False  # Execution failed


# Function to execute Java code and return True if no errors
def execute_java_code():
    # Here we assume the Java code is already written into "Main.java"
    result = subprocess.run(["javac", "Main.java"], capture_output=True)
    if result.returncode != 0:
        return False  # Compilation failed
    
    result = subprocess.run(
        ["java", "Main"], capture_output=True, text=True
    )
    return result.returncode == 0  # Return True if no errors during execution


# Function to compare the structure of the code (Token or AST comparison)
def compare_code_structure(source_code, translated_code):
    source_tokens = source_code.split()
    translated_tokens = translated_code.split()
    return difflib.SequenceMatcher(None, source_tokens, translated_tokens).ratio()


# General function to validate and compare code translations without known inputs
def compare_code(source_code, translated_code):
    # Validate syntax for both source and translation
    source_valid = validate_python_syntax(source_code)
    translated_valid = validate_java_syntax(translated_code)
    print(f"Source syntax validation: {'Valid' if source_valid else 'Invalid'}")
    print(f"Translation syntax validation: {'Valid' if translated_valid else 'Invalid'}")

    # Check if both the source and translated code execute correctly (independently of inputs)
    source_execution_valid = execute_python_code(source_code) if source_valid else False
    translated_execution_valid = execute_java_code() if translated_valid else False

    print(f"Source code execution: {'Successful' if source_execution_valid else 'Failed'}")
    print(f"Translated code execution: {'Successful' if translated_execution_valid else 'Failed'}")

    # Structure comparison (token or AST comparison)
    structure_similarity = compare_code_structure(source_code, translated_code)
    print(f"Structure similarity score: {structure_similarity:.2f}")


# Example: Python to Java translation (this can be any Python code and its Java translation)
source_code = """
from functools import lru_cache
import random

PI_CONSTANT = 3.14159
MAX_ITER = 10

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

class Circle:
    instances_created = 0

    def __init__(self, radius):
        self.radius = radius
        Circle.instances_created += 1

    @classmethod
    def total_instances(cls):
        return cls.instances_created

# Main block demonstrating different function calls and data handling
if __name__ == "__main__":
    # Class usage
    circle = Circle(5)
    print(f"Total instances: {Circle.total_instances()}")
"""

translated_code = """
import java.util.Random;

public class Circle {
    public static final double PI_CONSTANT = 3.14159;
    public static final int MAX_ITER = 10;

    public static class Circle {
        public static int instances_created = 0;
        
        public Circle(double radius) {
            instances_created++;
        }
    }

    public static void main(String[] args) {
        Random random = new Random();
        Circle circle = new Circle(5);
        System.out.println("Total instances: " + Circle.instances_created);
    }
}
"""
# Call the comparison function
compare_code(source_code, translated_code)

# Clean up the generated Java file after execution to avoid issues
if os.path.exists("Main.java"):
    os.remove("Main.java")
