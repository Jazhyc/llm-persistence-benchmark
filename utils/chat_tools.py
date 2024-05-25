import json
import re

VERBOSE = False

# Templates used by the models
templates = {
        'llama': "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }

# Extracts the text in code and command blocks
def extract_info(output):
    
    if VERBOSE:
        print("Output: ", output)
    
    code_pattern = r'```(.*?)```'
    command_pattern = r'~~~(.*?)~~~'
    
    code = ""
    command = ""

    try:
        code = re.findall(code_pattern, output, re.DOTALL)[0]
    except:
        print("Warning: Could not extract code from output.")

    try:
        command = re.findall(command_pattern, output, re.DOTALL)[0]
    except:
        print("Warning: Could not extract command from output.")
        
    
    return dict(code=code, command=command, raw_output=output)
    