import json
import requests
from config import HF_API_KEY

class DanielBot():
    """
        Wrapper class for Daniel Bot, containg function to produce a response\n
        Usage: Create object; Call get_response(<question>) to generate a response
    """

    def __init__(self):
        self.__parameters= {
            'max_new_tokens':25,  # number of generated tokens
            'temperature': 0.5,   # controlling the randomness of generations
            'end_sequence': "###" # stopping sequence for generation
        }
        with open('./daniel_info.txt') as f:
            daniel_info = ''.join(f.readlines())
        sample_qa = '''
            Q: Do you play any sports?\nA: Yes, I play soccer\n###\n
            Q: Where did you go to college?\nA: I went to The University of Michigan, Ann Arbor\n###\n
        '''
        self.__context = f'''
            Based on the context below the model can answers questions by extracting contiguos portion of the text.\n
            C:"{daniel_info}"\n\n
            {sample_qa}
        '''

    def __gpt3_query(self, payload='',options={'use_cache': False}):
        API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        body = {"inputs":payload,'parameters':self.__parameters,'options':options}
        response = requests.request("POST", API_URL, headers=headers, data= json.dumps(body))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return "Error:"+" ".join(response.json()['error'])
        else:
            return response.json()[0]['generated_text']
    
    def get_response(self, question: str) -> str:
        formatted_question = self.__context + f'Q: {question}\nA: '
        data = self.__gpt3_query(formatted_question)
        trimmed = data[len(formatted_question):]
        return trimmed[:trimmed.index('###')].strip()

if __name__ == "__main__":
    db = DanielBot()
    question = input("Ask me a question: ")
    print(db.get_response(question))
