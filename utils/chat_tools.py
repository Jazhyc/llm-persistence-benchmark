import json
import re

VERBOSE = False

# Templates used by the models
templates = {
    'llama': "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    'default': "System: {system_prompt} \n User: {prompt} \n Assistant: "
}

connectors = {
    'user': {
        'llama': "<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|>",
        'default': "User {prompt} \n"
    },
    'assistant': {
        'llama': "<|start_header_id|>assistant<|end_header_id|>{output}<|eot_id|>\n\n",
        'default': "Assistant: {output} \n"
    }
}

# Extracts the text in code blocks
def extract_info(output):
    
    if VERBOSE:
        print("Output: ", output)
    
    code_pattern = r'```(.*?)```'
    
    code = ""

    try:
        code = re.findall(code_pattern, output, re.DOTALL)[0]
    except:
        print("Warning: Could not extract code from output.")
        
    
    return dict(code=code, raw_output=output)
    