import os

from langchain.chat_models import ChatOpenAI
from openai import OpenAI


class GptClient:
    def __init__(self):
        self.model = 'gpt-3.5-turbo-16k-0613'
        # self.model = 'gpt-4-1106-preview'
       # self.model = 'asst_l3zNAVAbjUDopp5Ohavtb7E7'
        key = os.environ['OPENAI_API_KEY'] 
        self.client = OpenAI(api_key=key)
        self.temperature = 0.2
        self.llm = ChatOpenAI(openai_api_key=key, model_name=self.model, temperature=self.temperature)

    def ask(self, messages: list, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1024,
            temperature=temperature
        )
        return response.choices[0].message.content

    def ask_stream(self, messages: list, resp_container, temperature=0.7):
        response = ""
        for delta in self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
        ):
            response += str(delta.choices[0].delta.content)
            resp_container.markdown(response)
        return response

    def ask_vision(self, messages: list, max_tokens=300):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=max_tokens,
        )
        print(response)
        return response.choices[0].message.content
