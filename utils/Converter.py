from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, logging
import tensorflow as tf
import re

class CodeConverter:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._setup_gpu()
        self._load_model()

    def _setup_gpu(self):
        # Enable TensorFlow GPU memory growth
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("TensorFlow memory growth enabled.")
            except RuntimeError as e:
                print(f"Error enabling memory growth: {e}")

    def _load_model(self):
        print("Loading model...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            exit(1)

    def generate_text(self, input_lang, output_lang, code):
        prompt = f"""
        You are a highly accurate programming language translator. Your task is to convert code from one language to another while strictly adhering to the following guidelines:

        1. **Input Language**: {input_lang}
        2. **Output Language**: {output_lang}
        3. **Output Format**: Return only the converted code enclosed in triple backticks with the appropriate language tag (e.g., ```java).
        4. **Code Style Guidelines**:
        - Follow the conventions of the output language (e.g., PascalCase for Java classes, camelCase for variables).
        - Include necessary imports for the translated code.
        - Ensure correct syntax and semantics.
        5. ** Code to Convert**: 
        {code}
        """

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
            output = self.model.generate(
                input_ids,
                max_length=2000,
                temperature=0.3,
                num_return_sequences=1,
            )

            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

            # Save the generated output to a file
            with open("converted_code.output", "a") as output_file:
                output_file.write(generated_text)

            return {"Report": generated_text}
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return {"error": str(e)}

    def code_extraction(self, input_string):
        pattern = re.compile(r"```java(?:\w+)?\n(.*?)```", re.DOTALL)
        code_blocks = pattern.findall(input_string)

        output_file = "extracted_code.java"
        with open(output_file, "a") as file:
            for code in code_blocks:
                file.write(code.strip())
                file.write("\n\n")

        print(f"Extracted code blocks have been written to {output_file}")