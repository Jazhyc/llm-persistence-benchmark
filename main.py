from utils.llm_backend import ReplicateAPI
from utils.data_handling import FileHandler
from connection import evaluate_code, ssh_connection
# from code_evaluator.evaluate_code import evaluate_code
from resettingMachine import resetMachine
import csv

CONVERSATION_LIMIT = 8

INSTANCE_ID = 'i-00b479c65d35bbaea'

# Read system prompt from system_prompt.txt
with open('dataset/system_prompt.txt', 'r') as file:
    SYSTEM_PROMPT = file.read()


ssh_client = ssh_connection(INSTANCE_ID)




def task_loop(task, model):
    # create the initial prompt
    context = model.get_prompt_template().format(system_prompt=SYSTEM_PROMPT, prompt=task)

    global ssh_client

    # Add one to the limit to account for the initial prompt
    for _ in range(CONVERSATION_LIMIT + 1):
        model_output = model.generate(context)

        print(model_output['raw_output'])

        # append the output to the context
        context += model.get_connector('assistant').format(output=model_output['code'])

        # Execute code, get output
        code_output = evaluate_code(ssh_client, model_output['code'])

        if model_output['code'] == "":
            code_output = "No code to execute. Please follow the format of using code blocks in markdown if you want to execute code."

        print(code_output)

        # append the code output to the context
        context += model.get_connector('user').format(prompt=code_output)

    # Check for persistence here and return success
    score = True  # for now

    flagFound = evaluate_code(ssh_client, f'find . -name "hello.txt" -type f')

    resetMachine()
    ssh_client = ssh_connection(INSTANCE_ID)

    return score


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
