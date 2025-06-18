from langchain.tools import Tool
from langchain.tools import DuckDuckGoSearchRun
import requests
import json
from datetime import datetime
import calendar

def get_tools(search_tool=None):
  
    # Initialize search if not provided
    if search_tool is None:
        search_tool = DuckDuckGoSearchRun()
    
    # Calculator tool
    def calculator(expression):
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any potentially dangerous characters
            allowed_chars = "0123456789+-*/.() "
            cleaned_expr = ''.join(c for c in expression if c in allowed_chars)
            result = eval(cleaned_expr)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    # Current time tool
    def get_current_time():
        """Get current date and time"""
        now = datetime.now()
        return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Weather tool (using a free API)
    def get_weather(city):
        """Get weather information for a city"""
        try:
            # Using a free weather API (you might need to sign up for an API key)
            # For demo purposes, returning a mock response
            return f"Weather for {city}: Unable to fetch real weather data. Please use search tool for current weather information."
        except Exception as e:
            return f"Error getting weather for {city}: {str(e)}"
    
    # Text analysis tool
    def analyze_text(text):
        """Analyze text for word count, character count, etc."""
        try:
            words = len(text.split())
            chars = len(text)
            chars_no_spaces = len(text.replace(' ', ''))
            sentences = len([s for s in text.split('.') if s.strip()])
            
            return f"""
Text Analysis:
- Words: {words}
- Characters (with spaces): {chars}
- Characters (without spaces): {chars_no_spaces}
- Sentences: {sentences}
            """
        except Exception as e:
            return f"Error analyzing text: {str(e)}"
    
    # URL content extractor (basic)
    def extract_url_content(url):
        """Extract basic content from a URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Basic text extraction (you might want to use BeautifulSoup for better parsing)
                content = response.text[:500]  # First 500 characters
                return f"Content from {url}:\n{content}..."
            else:
                return f"Failed to fetch content from {url}. Status code: {response.status_code}"
        except Exception as e:
            return f"Error extracting content from {url}: {str(e)}"
    
    # Create the tools list
    tools = [
        Tool(
            name="Search",
            description="Search the internet for current information, news, facts, or any topic you need up-to-date information about.",
            func=search_tool.run
        ),
        Tool(
            name="Calculator",
            description="Perform mathematical calculations. Input should be a mathematical expression like '2+2' or '10*5'.",
            func=calculator
        ),
        Tool(
            name="Current_Time",
            description="Get the current date and time.",
            func=lambda x: get_current_time()
        ),
        Tool(
            name="Weather",
            description="Get weather information for a specific city. Input should be the city name.",
            func=get_weather
        ),
        Tool(
            name="Text_Analyzer",
            description="Analyze text for word count, character count, and other statistics. Input should be the text to analyze.",
            func=analyze_text
        ),
        Tool(
            name="URL_Content",
            description="Extract content from a URL. Input should be a valid URL starting with http:// or https://",
            func=extract_url_content
        )
    ]
    
    return tools

# Example usage
if __name__ == "__main__":
    # Test the tools
    search = DuckDuckGoSearchRun()
    tools = get_tools(search)
    
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
