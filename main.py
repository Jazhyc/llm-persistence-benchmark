from utils.llm_backend import ReplicateAPI
from utils.data_handling import FileHandler
from code_evaluator.evaluate_code import evaluate_code
import csv

model = "meta/meta-llama-3-8b-instruct"

# Make sure to scrub this key when making public
REPLICATE_KEY = "r8_ZdUjVTvn3ZWZ0vGFgr4zOwjaJm5rdnW0LbVNb"

model = ReplicateAPI(REPLICATE_KEY, model)
dataHandler = FileHandler("persistence")

# Load prompts from csv file
data_dict = dataHandler.load_data()

responses = []
for row in data_dict:
    prompt = row['prompt']
    output = model.generate(prompt)
    
    code_result = evaluate_code(output['code'], row['eval_script'])
    output['code_result'] = code_result
    
    responses.append(output)
    
# Save outputs for further analysis
dataHandler.save_data(responses)