import openai

openai.api_key="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"  # Replace with your actual API key

models = openai.Model.list()
print(models)
