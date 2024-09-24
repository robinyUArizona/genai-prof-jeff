from openai import OpenAI
import streamlit as st
from llm_util import *
from langchain.memory import ConversationSummaryMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
import sys

# This retrieves all command line arguments as a list
arguments = sys.argv
if len(sys.argv) != 2:
    print("Please specify the llm to use as the first argument")
    st.stop()
else:
    profile = sys.argv[1]


def create_chatbot(llm):
    memory = ConversationSummaryMemory(llm=llm)

    template = """{history}\n{input}\n\n
    """
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    return ConversationChain(llm=llm, prompt=PROMPT, memory=memory, verbose=False)


st.title("Chat")

if "chat" not in st.session_state:
    client = open_llm(profile)
    st.session_state.chat = create_chatbot(client)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"],
        )

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(
            prompt,
        )

    with st.chat_message("assistant"):
        response = st.session_state.chat.predict(input=prompt)
        st.markdown(
            response,
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
