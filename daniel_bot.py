import json
import requests
import os
from config import HF_API_KEY

def query(payload='',parameters=None,options={'use_cache': False}):
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    body = {"inputs":payload,'parameters':parameters,'options':options}
    response = requests.request("POST", API_URL, headers=headers, data= json.dumps(body))
    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError:
        return "Error:"+" ".join(response.json()['error'])
    else:
      return response.json()[0]['generated_text']

parameters = {
    'max_new_tokens':25,  # number of generated tokens
    'temperature': 0.5,   # controlling the randomness of generations
    'end_sequence': "###" # stopping sequence for generation
}

context  = ''
with open('./daniel_info.txt') as f:
    context += ''.join(f.readlines())

question = input('Type a question: ')
sample_qa = 'Q: Do you play any sports?\nA: Yes, I play soccer\n###\nQ: Where did you go to college?\nA: I went to The University of Michigan, Ann Arbor\n###\n'
prompt = f'Based on the context below the model can answers questions by extracting contiguos portion of the text.\nC:"{context}"\n\n{sample_qa}Q: {question}\nA:'
data = query(prompt,parameters)
trimmed = data[len(prompt)-2:]
print (trimmed[:trimmed.index('\n')])