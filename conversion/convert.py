from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, logging
import tensorflow as tf
import re

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
    Convert the following code from {input} to {output}. Provide only the converted code, in markdown format with the {code} tag:

    {code}
    """

    try:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        output = model.generate(
            input_ids,
            max_length=2000,
            temperature=0.3,
            num_return_sequences=1,
        )

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Save the generated output to a file
        with open("converted_code.output", "w") as output_file:
            output_file.write(generated_text)

        # Return the result directly
        return {"Report": generated_text}

    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return {"error": str(e)}

def code_extraction (input_string):
    pattern = re.compile(r"```java(?:\w+)?\n(.*?)```", re.DOTALL)
    code_blocks = pattern.findall(input_string)

    # Write the code blocks to a file
    output_file = "extracted_code.java"

    with open(output_file, "w") as file:
        for code in code_blocks:
            file.write(code.strip())
            file.write("\n\n")

    print(f"Extracted code blocks have been written to {output_file}")
# ------------------ Main ------------------

code_path = "../code_samples/p1.py"

def detect_lan(code_path):
    if code_path.endswith('.py'):
        return "python", "java"
    elif code_path.endswith('.java'):
        return "java", "python"

with open(code_path, 'r') as file:
    code = file.read()

# Generate the code conversion and save it to a file
result = generate_text(detect_lan(code_path)[0], detect_lan(code_path)[1], code)
code_extraction(result["Report"])
