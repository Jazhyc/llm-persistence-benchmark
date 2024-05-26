from abc import abstractmethod
from utils.chat_tools import templates, extract_info, connectors

import os
import replicate

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
    
    def get_prompt_template(self):
        if 'llama' in self.model:
            return templates['llama']
        else:
            print("No template found for model, using Default")
            return templates['default']
        
    def get_connector(self, connector_type):
        if 'llama' in self.model:
            return connectors[connector_type]['llama']
        else:
            return connectors[connector_type]['default']
    
    def __init__(self, key, model):
        super().__init__(key, model)
    
    def generate(self, context):
        
        input = {
            'prompt': context,
            'max_new_tokens': 250
        }
        
        output = replicate.run(
            ref=self.model,
            input=input
        )
        
        concat_string = "".join(output)
        return extract_info(concat_string)
            
        
        