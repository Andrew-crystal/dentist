import os
from functools import reduce
from io import BytesIO

import PyPDF2
import pinecone
import streamlit as st
from langchain.vectorstores import Pinecone

from src.config import *
from src.pinecone_dal import PineconeDal

load_dotenv()


def initialize():
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='gcp-starter')
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "vectordb" not in st.session_state:
        st.session_state.vectordb = None
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "login_id" not in st.session_state:
        st.session_state.login_id = "AnonymousUser"
    # else:
    #     st.toast(f"Current User is {st.session_state.login_id}")

def page_content():
    st.set_page_config(page_title="PDF UPLOADER")
    col1, col2 = st.columns(2)
    col2.markdown(f"Logged in as {st.session_state.login_id}")
    st.write("## Upload your PDF")
    st.session_state.uploaded_files = st.file_uploader("Choose PDF files you want to upload",
                                                       accept_multiple_files=True)
    if st.session_state.uploaded_files:
        print(f"uploaded files: {st.session_state.uploaded_files}")
    if st.button("Upload PDF Document"):
        handle_upload()

def handle_upload():
    st.markdown("Started parsing pdf files.")
    st.markdown(f"Logged in as **{st.session_state.login_id}**")
    extracted_data = {}

    # if os.getenv('PINECONE_INDEX') not in pinecone.list_indexes():
    #     pinecone.create_index(os.getenv('PINECONE_INDEX'), dimension=1536)
    pinecone_index = pinecone.Index(PineconeDal.index_name) # os.getenv('PINECONE_INDEX'))

    for file_idx in range(len(st.session_state.uploaded_files)):
        st.session_state.uploaded_files[file_idx].seek(0)
        st.markdown(f"Parsing {st.session_state.uploaded_files[file_idx].name}")

        # images = convert_from_bytes(st.session_state.uploaded_files[file_idx].getvalue())
        extracted_data[st.session_state.uploaded_files[file_idx].name] = ""
        pdf_stream = BytesIO(st.session_state.uploaded_files[file_idx].getvalue())
        pdf_reader = PyPDF2.PdfReader(pdf_stream)


        # Extract text
        st.markdown(f"Extracting text from PDF")
        for page in pdf_reader.pages:
            extracted_data[st.session_state.uploaded_files[file_idx].name] += page.extract_text()

        # img_byte_arr = []
        # for page_idx, image in enumerate(images):
        #     temp = io.BytesIO()
        #     image.save(temp, format='JPEG')
        #     print(f'page_idx is {page_idx}')
        #     # img_byte_arr.append(temp.getvalue())
        #     # extracted_data[st.session_state.uploaded_files[file_idx].name] += GGvision_client().detect_labels(temp.getvalue(), page_idx)
        #     extracted_data[st.session_state.uploaded_files[file_idx].name] += GptLogic().detect_labels([temp.getvalue()], page_idx)

    # using Chatgpt4 vision batch mode
    # extracted_text = GptLogic().detect_labels(img_byte_arr, i)
    st.markdown(f"Splitting text into chunks")
    for pdf_idx in extracted_data:
        extracted_data[pdf_idx] = txt_splitter.create_documents([extracted_data[pdf_idx]])

    st.markdown(f"calling reduce function")
    docs = reduce(lambda a, b: a + b, extracted_data.values())

    st.markdown(f"Embedding document into pinecone")
    st.session_state.vectordb = Pinecone.from_documents(docs, embeddings, index_name=PineconeDal.index_name,
                                                        namespace=f"{st.session_state.login_id}")
    st.session_state.retriever = st.session_state.vectordb.as_retriever()
    st.success(f"Success")


if __name__ == "__main__":
    initialize()
    page_content()
