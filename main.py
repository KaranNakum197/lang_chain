import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from agent_tools import get_tools

# Load API key
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("🚨 GOOGLE_API_KEY not found. Please check your .env or Streamlit secrets.")
    st.stop()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.5,
    google_api_key=google_api_key
)

# Tools
search = DuckDuckGoSearchRun()
tools = get_tools(search)

# Agent
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# Streamlit UI
st.set_page_config(page_title="Gemini ChatBot with Tools", page_icon="🧠")
st.title("🧠 Gemini ChatBot + Tools")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask me anything...")

if user_input:
    with st.spinner("Thinking..."):
        result = agent.run(user_input)
        st.session_state.history.append((user_input, result))

for q, a in st.session_state.history[::-1]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
