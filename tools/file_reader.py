from langchain.tools import Tool
from langchain.tools.python.tool import PythonREPLTool

def get_tools(search_tool):
    return [
        Tool(
            name="DuckDuckGo Search",
            func=search_tool.run,
            description="Useful for answering questions about current events or general knowledge."
        ),
        PythonREPLTool()
    ]
