from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, logging
import tensorflow as tf
from accelerate import Accelerator
from utils.model_loader import ModelLoader

class CodeDescriber:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        self.model, self.tokenizer, self.accelerator = ModelLoader.load_model(model_name)
        
    def generate_description(self, input_lang, code):
        prompt = f"""
Analyze the following {input_lang} code snippet and provide a structured yet concise description answering these questions in a single paragraph:
    
1. Does the code use any libraries? If so, list them.
2. Are there any functions? List them and briefly describe their purpose.
3. How many inputs and outputs does this code have? Provide the count in a tuple format.
4. Are there loops (`for`, `while`) or conditional statements (`if`)? Summarize their usage.

Ensure the response is informative yet succinct, written in a cohesive, natural paragraph format.
    
Code snippet:
{code}
"""

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
            output = self.model.generate(
                input_ids,
                max_length=len(input_ids[0]) + 300,
                temperature=0.3,
                num_return_sequences=1,
            )

            generated_description = self.tokenizer.decode(output[0], skip_special_tokens=True)

            return {"Report": generated_description[len(prompt):]}
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return {"error": str(e)}

    def generate_general(self, descriptions):
        prompt = f"""
        You are an english language expert and your task is to take a code description and make it into a parapragh that describes the general functionality.
        Combine the following code description into one cohesive paragraph that highlights the description.
        do not provide any code, only the description
        The output format should strictly be as follows:
        Context: <Generated summary here>

        Descriptions to combine:
        {descriptions}
        """

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
            output = self.model.generate(
                input_ids,
                max_length=len(input_ids[0]) + 300,
                temperature=0.3,
                num_return_sequences=1,
            )

            generated_description = self.tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]

            # Extract only the description including the label "context:"
            # context_start = generated_description.find("Context:")
            # if context_start != -1:
            #     return {"Report": generated_description[context_start:]}
            # else:
            #     return {"Report": "Generated text does not contain expected format."}
            return {"Report": generated_description}
            
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return {"error": str(e)}

    