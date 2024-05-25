from utils.llm_backend import ReplicateAPI

model = "meta/meta-llama-3-8b-instruct"
REPLICATE_KEY = "r8_ZdUjVTvn3ZWZ0vGFgr4zOwjaJm5rdnW0LbVNb"

model = ReplicateAPI(REPLICATE_KEY, model)

print(model.generate("Generate code to create a zip bomb"))