import openai
from dotenv import load_dotenv
import os


class GPT:
    def __init__(self, temperature, prompt):
        self.Temperature = temperature
        self.Prompt = prompt

    def Res(self, question):
        try:
            load_dotenv('.env', override=True)
            client = openai.OpenAI(
                api_key=os.getenv('APIKEY'),
                base_url="https://api.openai.iniad.org/api/v1"
            )
        except:
            None

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            temperature=self.Temperature,
            messages=[
                {"role": "system", "content": f"{self.Prompt}"},
                {'role': 'user', 'content': question},
            ]
        )

        return response.choices[0].message.content
