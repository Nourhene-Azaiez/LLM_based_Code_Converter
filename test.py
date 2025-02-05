
from utils.Comparator import CodeComparator


def test_syntax_validators():
    test_cases = {
        "python": "print('Hello, world!')",
        "java": "public class Test { public static void main(String[] args) { System.out.println(\"Hello, world!\"); } }",
        "javascript": "console.log('Hello, world!');",
        "typescript": "let message: string = 'Hello, world!'; console.log(message);",
        "css": "body { background-color: blue; }",
        "ruby": "puts 'Hello, world!'",
        "php": "<?php echo 'Hello, world!'; ?>"
    }
    
    for lang, code in test_cases.items():
        validator = getattr(CodeComparator, f"validate_{lang}_syntax", None)
        if validator:
            print(f"Testing {lang.capitalize()}: {'Pass' if validator(code) else 'Fail'}")

if __name__ == "__main__":
    test_syntax_validators()
