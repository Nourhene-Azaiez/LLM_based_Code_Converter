from accelerate import Accelerator
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, logging
import tensorflow as tf
import re
from utils.model_loader import ModelLoader

class CodeConverter:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        self.model, self.tokenizer, self.accelerator = ModelLoader.load_model(model_name)
        
    def generate_text(self, input_lang, output_lang, code):
        prompt = f"""
        You are a highly accurate programming language translator. Your task is to convert code from one language to another while strictly adhering to the following guidelines:

        1. **Input Language**: {input_lang}
        2. **Output Language**: {output_lang}
        3. **Output Format**:
        - Return only the converted code enclosed in triple backticks with the appropriate language tag (e.g., ```{output_lang.lower()} or ```{input_lang.lower()}).
        - The output should have only one code block with the converted code.
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

    def code_extraction(self, input_string,output_lang):
        pattern = re.compile(r"```" + re.escape(output_lang.lower()) + r"(?:\w+)?\n(.*?)```", re.DOTALL)
        code_blocks = pattern.findall(input_string)

        translated_code=""""""
        for code in code_blocks:
            translated_code+= code
            translated_code+= "\n"
        
        return translated_code