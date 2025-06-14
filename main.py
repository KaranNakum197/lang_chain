import os
import streamlit as st
import langchain_community
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from agent_tools import get_tools

load_dotenv()
llm = ChatOpenAI(temperature=0)

search = DuckDuckGoSearchRun()
tools = get_tools(search)

agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

st.set_page_config(page_title="ChatGPT with Tools", page_icon="🤖")
st.title("🧠 ChatGPT with Tools")
st.markdown("Ask anything. It can calculate, search, and reason!")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Your Question")

if user_input:
    with st.spinner("Thinking..."):
        result = agent.run(user_input)
        st.session_state.history.append((user_input, result))

for q, a in st.session_state.history[::-1]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
