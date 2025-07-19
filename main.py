import asyncio
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import ShellTool
# from langchain_core.tools import Tool
from langchain.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Enable detailed logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("langchain")
logger.setLevel(logging.DEBUG)

python_repl = PythonREPL()

@tool()
def run_python_code(code: str) -> str:
    """Executes Python code and returns the result."""
    return python_repl.run(code)


async def main():
    shell_tool = ShellTool()

    mcp_connections = {
        # "selenium": {
        #     "command": "npx",
        #     "args": ["-y", "@angiejones/mcp-selenium"],
        #     "transport": "stdio",
        # },
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
            "transport": "stdio",
        }
    }

    client = MultiServerMCPClient(mcp_connections)

    # async with client.session("selenium") as session:
    #     # selenium_tools = await client.get_tools(server_name="selenium")
    #     selenium_tools = await load_mcp_tools(session)
    #     # Use selenium_tools here for all browser actions
    
    async with client.session("playwright") as session:
        playwright_tools = await load_mcp_tools(session)

        # all_tools = [shell_tool, run_python_code] + selenium_tools + playwright_tools

        all_tools = [shell_tool, run_python_code] + playwright_tools

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        agent = create_react_agent(llm, all_tools)

        sop_document_text = """
        Please perform the following SOP:
        1. Open https://www.accuweather.com/en/in/hyderabad/202190/weather-forecast/202190 in the browser.
        2. Check what is the weather in Hyderabad wait until you get the weather in Hyderabad, if you are not able to fetch the data using elements try to read the html text and get the data.
        3. Run a shell command to list files in the current directory.
        4. Fetch the page title and weather in Hyderabad and create a markdown file with the title and weather in the current directory.
        """

        print("Starting agent with SOP document...")

        # Stream the agent output to see intermediate steps
        async for step in agent.astream({"messages": [{"role": "user", "content": sop_document_text}]}, stream_mode="updates"):

            # step is a dict with keys like 'agent' and 'tools' containing messages
            print("Step update:")
            print(step)

        print("Agent run complete.")

if __name__ == "__main__":
    asyncio.run(main())
