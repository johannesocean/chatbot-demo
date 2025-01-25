import streamlit as st
from decouple import config
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from vectorstore import query_collection
from utils import construct_source_material, Message, TEMPLATE, get_history_str

COLLECTION_NAME = "collection-name"


@st.cache_resource
def get_llm():
    return ChatOpenAI(
        api_key=config("OPENAI_API_KEY"),
        model_name=config("OPENAI_MODEL"),
        streaming=True, temperature=0
    )


llm = get_llm()

st.title(":male-cook: Master Chef Recipe Chatbot :tomato:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if prompt := st.chat_input("What kind of food would you like to cook today?"):

    history_str = get_history_str(st.session_state.messages)

    st.session_state.messages.append(Message(role="user", content=prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    query_result = query_collection(prompt)
    source_material = construct_source_material(query_result)

    with st.chat_message("assistant", avatar="👨‍🍳"):
        response = st.write_stream(
            llm.stream(
                [
                    SystemMessage(content=TEMPLATE.format(context_str=source_material, history_str=history_str)),
                    HumanMessage(content=prompt)
                ]
            )
        )

    st.session_state.messages.append(Message(role="assistant", content=response))
