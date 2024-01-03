from dotenv import load_dotenv


from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()

embeddings = OpenAIEmbeddings()
txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=160000,
        chunk_overlap=200
    )

