from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPEN_AI_API_KEY")

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

    def chatbot():
        uploaded_file = st.file_uploader("UFC 데이터 파일 업로드 (CSV, JSON)", type=['csv'])

        if uploaded_file is not None:
            if uploaded_file.type == 'application/vnd.ms-excel':
                df = pd.read_csv(uploaded_file)
                content = df.to_string(index=False)
            elif uploaded_file.type == 'application/json':
                df = pd.read_json(uploaded_file)
                content = df.to_string(index=False)
        else:
            content = ""
            
        want_to = """너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
        content
        {}
        """

        MODEL = st.sidebar.selectbox(
            "ChatGPT 모델 선택",
            ["gpt-4-0125-preview", "gpt-4-turbo-preview" , "gpt-4-1106-preview", "gpt-3.5-turbo-0125", "gpt-3.5-turbo", "gpt-3.5-turbo-1106"],
            index=0
        )

        st.header("나만의 챗봇 서비스")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [ChatMessage(role="assistant", content="안녕하세요! 무엇이든 물어보세요!")]

        for msg in st.session_state.messages:
            st.chat_message(msg.role).write(msg.content)


        if prompt := st.chat_input("챗봇과 대화해보세요..."):
            st.session_state.messages.append(ChatMessage(role="user", content=prompt))
            st.chat_message("user").write(prompt)

            if not API_KEY:
                st.info("OpenAI API 키를 추가해주세요.")
                st.stop()

            with st.chat_message("assistant"):
                stream_handler = StreamHandler(st.empty())
                llm = ChatOpenAI(openai_api_key=API_KEY, streaming=True, callbacks=[stream_handler], model_name=MODEL)
                response = llm([ChatMessage(role="system", content=want_to.format(content))] + st.session_state.messages)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
