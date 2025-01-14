import os
import ast
import subprocess
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from bert_score import score

# Dataset containing source code and translations
dataset = [
    {
        "source": """ 
        import java.util.concurrent.ConcurrentHashMap;
        import java.util.concurrent.ConcurrentMap;
        import java.util.function.Function;

public class Circle {
            private static int instancesCreated = 0;
            private double radius;
            private static final double PI_CONSTANT = 3.14159;

            @FunctionalInterface
            public interface FunctionWithCache<T, R> {
                R apply(T t);
            }

            public static class FunctionWithCacheImpl<T, R> implements FunctionWithCache<T, R> {
                private final Function<T, R> func;

                public FunctionWithCacheImpl(Function<T, R> func) {
                    this.func = func;
                }

                @Override
                public R apply(T t) {
                    return func.apply(t);
                }
            }

            public Circle(double radius) {
                this.radius = radius;
                instancesCreated++;
            }

            public double calculateArea(double radius) {
                return PI_CONSTANT * radius * radius;
            }

            @Override
            public String toString() {
                return "Circle with radius " + radius;
            }

            public static int getInstancesCreated() {
                return instancesCreated;
            }

            public static void main(String[] args) {
                Circle circle = new Circle(5);
                System.out.println(circle);
                System.out.println(circle.calculateArea(5));
                System.out.println(Circle.getInstancesCreated());
            }
        }

        import java.util.Collections;

        public class Circle {
            private static int instancesCreated = 0;

            public Circle(int radius) {
                this.radius = radius;
                instancesCreated++;
            }

            public static int totalInstances() {
                return instancesCreated;
            }

            public static void main(String[] args) {
                Circle circle = new Circle(5);
                System.out.println("Total instances: " + Circle.totalInstances());
            }
        }
                """,
                "translation": """from functools import lru_cache
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
            print(f"Total instances: {Circle.total_instances()}")"""
    },
    # Add more examples here
]


def validate_python_syntax(code):
    """
    Validate Python syntax using the AST parser.
    """
    try:
        ast.parse(code)
        return 1
    except SyntaxError as e:
        return 0


def validate_java_syntax(code):
    """
    Validate Java syntax using the `javac` command.
    """
    try:
        class_name = extract_class_name(code)
        file_name = f"{class_name}.java"
        with open(file_name, "w") as f:
            f.write(code)
        result = subprocess.run(["javac", file_name], capture_output=True, text=True)
        if result.returncode == 0:
            return 1
        else:
            return 0
    finally:
        # Cleanup temporary file
        if os.path.exists(file_name):
            os.remove(file_name)

def compute_bertscore(reference, candidate):
    P, R, F1 = score([candidate], [reference], lang='en')
    return F1.mean().item()

def extract_class_name(code):
    """
    Extract the public class name from Java code.
    """
    for line in code.splitlines():
        if line.strip().startswith("public class"):
            return line.split()[2]
    return "Main"

def compute_composite_score(source_syntax_score, translate_syntax_score, bleu_score, source_syntax_weight=0.1, translate_syntax_weight=0.3, bleu_weight=0.6):
    """
    Compute a composite score by combining individual scores with weights.
    """
    return (source_syntax_score * source_syntax_weight) + (translate_syntax_score * translate_syntax_weight) + (bleu_score * bleu_weight)

# Main Script Execution

source = dataset[0]["source"]
translation = dataset[0]["translation"]

source_lang="python"
# Syntax validation
if source_lang == "python":
    source_syntax_score = validate_python_syntax(source)
    translate_syntax_score = validate_java_syntax(translation)
else:
    source_syntax_score= validate_java_syntax(source)
    translate_syntax_score= validate_python_syntax(translation)

# BLEU score

bleu_score = compute_bertscore(translation, source)
print(f"BLEU score: {bleu_score:.2f}")

composite_score = compute_composite_score(source_syntax_score,translate_syntax_score, bleu_score)
print(f"Composite Score: {composite_score:.2f}")

print("-" * 50)
