import time
import pinecone
import os

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.vectorstores import Pinecone

from src.config import *
# from src.gpt_logic import GptLogic
from src.gpt_client import GptClient
from src.pinecone_dal import PineconeDal

load_dotenv()


def initialize():
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='gcp-starter')
    if "login_id" not in st.session_state:
        st.session_state.login_id = "AnonymousUser"
    # else:
    #     st.toast(f"Current User is {st.session_state.login_id}")


initialize()


def page_header():
    st.write("## My Dentist")
    col1, col2 = st.columns(2)
    col2.write(f"Logged in as {st.session_state.login_id}")
    st.write("Welcome to My Dentist, your personal expert dentist. Please ask me anything about your dental health.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": """
Here are some good questions to ask me, your expert dentist:

- What are the signs of gum disease, and how can it be prevented?
- How often should I replace my toothbrush, and what kind should I use?
- Can you explain the proper technique for brushing and flossing?
- What are the best ways to whiten my teeth safely?
- Are there any dental procedures that can improve the appearance of my smile?
- How can I manage dental anxiety before a dentist appointment?
- What are the effects of diet on oral health?
- How can I protect my children's teeth from cavities?
- What should I do in case of a dental emergency, like a knocked-out tooth?
- Can you provide tips for maintaining good oral hygiene with braces or other orthodontic appliances?

Feel free to ask any of these questions, and I'd be happy to provide you with detailed answers!
        """}]


def render():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


def page_content():
    render()
    if user_question := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.chat_message("user").write(user_question)
        with st.chat_message("assistant"):
            resp_container = st.empty()
            # ai_response = GptLogic().my_dentist_response_stream(resp_container, user_question)
            ai_response = st.session_state.chain.run({'question': user_question})
            full_response = ""
            # Simulate stream of response with milliseconds delay
            # for chunk in ai_response.split(" "):
            #     full_response += chunk + " "
            #     time.sleep(0.02)
            #     # Add a blinking cursor to simulate typing
            #     resp_container.markdown(full_response + "|")
            resp_container.markdown(ai_response)
            print("AI response: ", ai_response)
            msg = {"role": "assistant", "content": ai_response}
            st.session_state.messages.append(msg)
            # .write(msg["content"])


if __name__ == "__main__":
    # st.set_page_config(page_title="My Dentist")

    # show_user_header()

    st.session_state.vectordb = Pinecone.from_documents([], embeddings, index_name=PineconeDal.index_name,
                                                        namespace=st.session_state.login_id)

    st.session_state.retriever = st.session_state.vectordb.as_retriever()

    # Create memory 'chat_history'
    st.session_state.memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history")

    # Create system prompt
    ki = " You are given the following extracted parts of a long document and a question. Provide a conversational answer. If you don't know the answer, just say 'Sorry, I don't know ... 😔.     Don't try to make up an answer."""
    template = """
        You are an AI assistant for answering questions.
       
        {context}
        Question: {question}
        Helpful Answer:"""

    st.session_state.chain = ConversationalRetrievalChain.from_llm(GptClient().llm,
                                                                   retriever=st.session_state.retriever,
                                                                   memory=st.session_state.memory,
                                                                   get_chat_history=lambda h: h,
                                                                   verbose=True)
    prompt_template = PromptTemplate(input_variables=["context", "question"], template=template)
    st.session_state.chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=prompt_template)
    page_header()
    page_content()
