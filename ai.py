# AI model handling (loading, response generation)
from transformers import TFAutoModelForCausalLM, AutoTokenizer

class AIModel:
    def __init__(self):
        # Load the tokenizer and the model using TensorFlow
        self.tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-j-6B')
        self.model = TFAutoModelForCausalLM.from_pretrained('EleutherAI/gpt-j-6B')

    def generate_response(self, prompt):
        # Tokenize the input prompt
        inputs = self.tokenizer(prompt, return_tensors="tf")
        # Generate the response
        outputs = self.model.generate(inputs['input_ids'], max_length=150)
        # Decode the output into text
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
