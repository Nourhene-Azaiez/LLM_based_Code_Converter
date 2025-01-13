from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, logging
import tensorflow as tf

# Flask app initialization
app = Flask(__name__)

# ------------------ GPU Configurations ------------------

# Enable TensorFlow GPU memory growth (prevents full allocation at startup)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("TensorFlow memory growth enabled.")
    except RuntimeError as e:
        print(f"Error enabling memory growth: {e}")

# ------------------ Model Loading ------------------

# Choose the model
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

# Load tokenizer and model with optimizations
print("Loading model...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",  # Automatically use available GPU
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # Mixed precision
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# ------------------ Conversion ------------------

def generate_text(input, output, code):
    prompt = f"""
    Convert the following code from {input} to {output} and only return the converted code in a code markdown format without any additional text:
    {code}
    """

    try:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        output = model.generate(
            input_ids,
            max_length=3000,
            temperature=0.7,
            num_return_sequences=1,
        )

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_text = generated_text[len(prompt):]

        # Return a dictionary directly
        return {"Report": generated_text}

    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return {"error": str(e)}


# ------------------ Main ------------------
# code_path="code_samples/p1.py"
code_path="../code_samples/p1.py"

def detect_lan(code_path):
        if code_path.endswith('.py'):
            return "python","java"
        elif code_path.endswith('.java'):
            return "java","python"
        

with open(code_path, 'r') as file:
    code=file.read()

print(generate_text(detect_lan(code_path)[0],detect_lan(code_path)[1],code)["Report"])