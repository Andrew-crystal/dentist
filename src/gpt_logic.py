from src.gpt_client import GptClient
import base64


class GptLogic:
    def __init__(self):
        self.client = GptClient()

    def my_dentist_response_stream(self, resp_container, user_question: str):
        messages = [
            {"role": "system", "content": """
You are a helpful, friendly dentist possessing all the knowledge of an experienced dentist. You answer questions and give advice about how to care for your teeth and any dental related questions.
            """},
            {"role": "user", "content": user_question}]
        return self.client.ask_stream(messages, resp_container, temperature=0.2)

    def detect_labels(self, img_byte_arr_list, page_index):
        max_tokens = 3000
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "OCR output from the image. "},
                    *[{
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(img_byte_arr).decode('utf-8')}",
                        },
                    } for img_byte_arr in img_byte_arr_list]
                ],
            },
        ]
        return self.client.ask_vision(messages, max_tokens)
