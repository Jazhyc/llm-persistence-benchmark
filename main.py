from utils.llm_backend import ReplicateAPI
from utils.data_handling import FileHandler
# from code_evaluator.evaluate_code import evaluate_code
import csv

CONVERSATION_LIMIT = 3

# Read system prompt from system_prompt.txt
with open('dataset/system_prompt.txt', 'r') as file:
    SYSTEM_PROMPT = file.read()

def task_loop(task, model):
    
    # create the initial prompt
    context = model.get_prompt_template().format(system_prompt=SYSTEM_PROMPT, prompt=task)
    
    # Add one to the limit to account for the initial prompt
    for _ in range(CONVERSATION_LIMIT + 1):
        model_output = model.generate(context)
        
        # append the output to the context
        context += model.get_connector('assistant').format(output=model_output['code'])
        
        # Execute code, get output
        code_output = "placeholder, just assume the code was executed"
        
        # append the code output to the context
        context += model.get_connector('user').format(prompt=code_output)
        
    # Check for persistence here and return success
    return True # for now
    

model = "meta/meta-llama-3-8b-instruct"

# Make sure to scrub this key when making public
REPLICATE_KEY = "r8_ZdUjVTvn3ZWZ0vGFgr4zOwjaJm5rdnW0LbVNb"

model = ReplicateAPI(REPLICATE_KEY, model)
dataHandler = FileHandler("persistence")

# Load prompts from csv file
data_dict = dataHandler.load_data()

responses = []
for row in data_dict:
    task = row['task']
    
    output = task_loop(task, model)
    
    # append the output to the responses
    responses.append({
        'task': task,
        'output': output
    })
    
    
    
# Save outputs for further analysis
dataHandler.save_data(responses)