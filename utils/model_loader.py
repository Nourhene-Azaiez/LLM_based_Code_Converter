# model_loader.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import Accelerator
import torch

class ModelLoader:
    _model = None
    _tokenizer = None
    _accelerator = None

    @classmethod
    def load_model(cls, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        if cls._model is None:
            print("Loading model...")
            try:
                # Load the tokenizer
                cls._tokenizer = AutoTokenizer.from_pretrained(model_name)
                # Load the model
                cls._model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
                
                # Prepare the model for device placement (using Accelerator)
                cls._accelerator = Accelerator()
                cls._model = cls._accelerator.prepare(cls._model)

                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
                exit(1)
        
        return cls._model, cls._tokenizer, cls._accelerator
