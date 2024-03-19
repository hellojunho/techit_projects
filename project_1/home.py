from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
import tempfile
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def run_home():
    st.title("ChatPDF")
    st.write("#### ChatPDF는 PDF 파일의 내용을 바탕으로 대화할 수 있습니다.")
    st.write("---")

    # 파일 업로드
    uploaded_file = st.file_uploader("Choose a file")
    st.write("---")

    def pdf_to_document(uploaded_file):
        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_filepath, "wb") as f:
            f.write(uploaded_file.getvalue())
        loader = PyPDFLoader(temp_filepath)
        pages = loader.load_and_split()
        return pages

    # 업로드 되면 동작하는 코드
    if uploaded_file is not None:
        pages = pdf_to_document(uploaded_file)

        # Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.split_documents(pages)

        # Embedding
        embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # load it into Chroma
        db = Chroma.from_documents(texts, embeddings_model)

        # Question
        st.header("PDF를 바탕으로 질문을 해보세요.")
        question = st.text_input('질문 입력')

        if st.button('질문하기'):
            with st.spinner('잠시만 기다려주세요...'):
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
                qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
                result = qa_chain({"query": question})
                st.write(result["result"])
