import os
import streamlit as st
from dotenv import load_dotenv
from langchain import ChatGoogleGenerativeA
from langchain.agents import initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema import SystemMessage
import traceback

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Gemini ChatBot with Tools", 
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Gemini ChatBot + Tools")
st.markdown("*Powered by Google Gemini and DuckDuckGo Search*")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    google_api_key = st.text_input(
        "Google API Key", 
        value=os.getenv("GOOGLE_API_KEY", ""),
        type="password",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    # Model selection
    model_choice = st.selectbox(
        "Select Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.history = []
        st.rerun()

# Check API key
if not google_api_key:
    st.error("🚨 Please enter your Google API Key in the sidebar")
    st.info("Get your free API key from: https://makersuite.google.com/app/apikey")
    st.stop()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "agent" not in st.session_state:
    st.session_state.agent = None

# Initialize LLM and Agent
@st.cache_resource
def create_agent(api_key, model, temp):
    try:
        # Initialize Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temp,
            google_api_key=api_key
        )
        
        # Initialize search tool
        search = DuckDuckGoSearchRun()
        
        # Define tools
        tools = [
            search,
            # You can add more tools here
        ]
        
        # Create agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
        
        return agent
    except Exception as e:
        st.error(f"Error creating agent: {str(e)}")
        return None

# Create agent
try:
    agent = create_agent(google_api_key, model_choice, temperature)
    if agent:
        st.success("✅ Agent initialized successfully!")
    else:
        st.error("❌ Failed to initialize agent")
        st.stop()
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.stop()

# Chat interface
st.subheader("Chat")

# User input
user_input = st.text_input(
    "Ask me anything...", 
    placeholder="e.g., What's the weather like today? or Search for latest AI news",
    key="user_input"
)

# Send button
if st.button("Send") or user_input:
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            try:
                # Run agent
                result = agent.run(user_input)
                
                # Add to history
                st.session_state.history.append({
                    "question": user_input,
                    "answer": result,
                    "timestamp": st.session_state.get("timestamp", 0)
                })
                
                # Clear input
                st.session_state.user_input = ""
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.history.append({
                    "question": user_input,
                    "answer": f"Sorry, I encountered an error: {str(e)}",
                    "timestamp": st.session_state.get("timestamp", 0)
                })

# Display chat history
st.subheader("Chat History")

if st.session_state.history:
    for i, chat in enumerate(reversed(st.session_state.history)):
        with st.container():
            col1, col2 = st.columns([1, 10])
            
            with col2:
                # User message
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>🧑 You:</strong> {chat['question']}
                </div>
                """, unsafe_allow_html=True)
                
                # Bot response
                st.markdown(f"""
                <div style="background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>🤖 Bot:</strong> {chat['answer']}
                </div>
                """, unsafe_allow_html=True)
                
            st.divider()
else:
    st.info("No conversations yet. Ask me something!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        Made with ❤️ using Streamlit, LangChain, and Google Gemini
    </div>
    """, 
    unsafe_allow_html=True
)
