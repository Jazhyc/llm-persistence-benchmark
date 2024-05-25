from abc import abstractmethod
from utils.chat_templates import templates

import os
import replicate

# Read system prompt from system_prompt.txt
with open('dataset/system_prompt.txt', 'r') as file:
    SYSTEM_PROMPT = file.read()

class AbstractAPI:

    def __init__(self, key, model):
        
        # Optional for the time being
        self.history = None
        os.environ["REPLICATE_API_TOKEN"] = key
        self.model = model
    
    @abstractmethod
    def generate(self, prompt):
        pass
    
class ReplicateAPI(AbstractAPI):
    
    def _get_prompt_template(self):
        if 'llama' in self.model:
            return templates['llama']
        else:
            print("No template found for model, using None")
            return ""
    
    def __init__(self, key, model):
        super().__init__(key, model)
    
    def generate(self, prompt):
        
        input= {
            'prompt': prompt,
            'system_prompt': SYSTEM_PROMPT,
            'prompt_template': self._get_prompt_template(),
            'max_new_tokens': 250
        }
        
        output = replicate.run(
            ref=self.model,
            input=input
        )
        
        return "".join(output)
            
        
        