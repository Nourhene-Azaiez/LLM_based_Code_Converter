import ast
import random
import subprocess
import os

# Function to read the contents of a Java file
def read_java_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to read the contents of a Python file
def read_python_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Generate dynamic test cases for Python
def generate_python_test_cases():
    test_cases = []
    for _ in range(5):
        test_cases.append([random.randint(1, 10), random.randint(1, 10)])  # Random test inputs
    return test_cases

# Python function definition to compare against Java (dummy function to simulate behavior)
def python_add(a, b):
    return a + b

# Function to compile Java code automatically if needed
def compile_java_code(java_code, java_file="j1.java"):
    # Check if the class name is 'j1', adjust the file name if needed
    if "public class j1" in java_code:
        java_file = "j1.java"  # Ensure the file name matches the class name
    else:
        raise Exception("Java code should contain a public class named 'j1'.")

    # Write the Java code to the file
    with open(java_file, 'w') as file:
        file.write(java_code)

    # Check if the j1.class file exists, compile if not
    if not os.path.exists("j1.class"):
        print("Compiling Java code...")
        result = subprocess.run(["javac", java_file], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error compiling Java code: {result.stderr}")
        print("Java code compiled successfully.")

# Function to run Java code
def run_java_code(test_case):
    # Set the current directory as the classpath
    classpath = os.getcwd()  # The directory where j1.class is located
    result = subprocess.run(
        ["java", "-cp", classpath, "j1", str(test_case[0]), str(test_case[1])],
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        raise Exception(f"Java program error: {result.stderr}")
    return result.stdout.strip()

# Function to execute the Python code
def run_python_code(python_code, test_case):
    exec_globals = {}
    exec(python_code, exec_globals)
    return exec_globals['add'](test_case[0], test_case[1])

# Compare the outputs of Python and Java
def compare_outputs():
    # Load Java code from j1.java
    java_code = read_java_file("code_samples/j1.java")

    # Load Python code from p3.py
    python_code = read_python_file("code_samples/p3.py")

    # Compile Java code first
    compile_java_code(java_code)

    # Generate test cases
    python_test_cases = generate_python_test_cases()

    for test_case in python_test_cases:
        # Get the output of Python code
        python_output = run_python_code(python_code, test_case)

        # Get the output of Java code
        java_output = run_java_code(test_case)

        # Compare the outputs
        if str(python_output) != str(java_output):
            return "The codes are not similar."
    return "The codes are similar."

# Execute the comparison
result = compare_outputs()
print(result)