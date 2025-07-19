import asyncio
import logging
from typing import Annotated, Literal
from dotenv import load_dotenv
from IPython.display import Image, display
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.graph import StateGraph, START, MessagesState, END
from langgraph.types import Command

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage
from langchain_community.tools import ShellTool
from langchain_experimental.utilities import PythonREPL

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("langchain")
logger.setLevel(logging.DEBUG)

# Instantiate Shell and Python REPL tools
shell_tool = ShellTool()
python_repl = PythonREPL()

@tool()
def run_python_code(code: str) -> str:
    """Execute Python code and return output."""
    return python_repl.run(code)

# Create generic handoff tool for agent transitions
def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer control to {agent_name} agent."

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )
    return handoff_tool

# Main agent: executes SOP steps and logs actions
async def main_agent(state: MessagesState) -> Command[Literal["critic_agent", "end"]]:
    messages = state["messages"]
    sop_document = state.get("sop_document", "")

    # Here you would implement actual SOP execution logic using tools
    # For demo, simulate an action log
    action_log = "Main agent performed a step according to SOP."

    new_message = {"role": "assistant", "content": action_log}
    updated_messages = messages + [new_message]

    # After action, handoff to critic for review
    return Command(
        goto="critic_agent",
        update={"messages": updated_messages, "sop_document": sop_document}
    )



async def critic_agent(state: MessagesState) -> Command[Literal["main_agent", "end"]]:
    messages = state["messages"]
    sop_document = state.get("sop_document", "")

    last_action = messages[-1].content if messages else ""

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    prompt = f"""
    You are a critic agent. The SOP document is: {sop_document}

    The main agent performed this action: {last_action}

    Please evaluate if this action aligns with the SOP. If it does, respond with "OK". If it does not, suggest alternative approaches or corrections for the main agent to try.
    """

    # Use HumanMessage instead of dict
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    critique = response.content if hasattr(response, "content") else "No critique."

    new_message = {"role": "assistant", "content": f"Critic feedback: {critique}"}
    updated_messages = messages + [new_message]

    if critique.strip().lower() == "ok":
        return Command(goto="end", update={"messages": updated_messages})
    else:
        return Command(goto="main_agent", update={"messages": updated_messages})


# Main async function to setup and run the multi-agent graph
async def main():
    mcp_connections = {
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
            "transport": "stdio",
        }
    }
    client = MultiServerMCPClient(mcp_connections)

    async with client.session("playwright") as session:
        playwright_tools = await load_mcp_tools(session)

        # Create handoff tools
        handoff_to_critic = create_handoff_tool(agent_name="critic_agent")
        handoff_to_main = create_handoff_tool(agent_name="main_agent")

        # Combine all tools
        all_tools = playwright_tools + [shell_tool, run_python_code, handoff_to_critic, handoff_to_main]

        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

        # Create react agents for main and critic
        main_react_agent = create_react_agent(llm, all_tools, name="main_agent")
        critic_react_agent = create_react_agent(llm, all_tools, name="critic_agent")

        # Build multi-agent graph
        graph = (
            StateGraph(MessagesState)
            .add_node(main_react_agent, name="main_agent", destinations=["critic_agent", END])
            .add_node(critic_react_agent, name="critic_agent", destinations=["main_agent", END])
            .add_edge(START, "main_agent")
            .add_edge("main_agent", "critic_agent")
            .add_edge("main_agent", END)
            .add_edge("critic_agent", "main_agent")
            .add_edge("critic_agent", END)
            .compile()
        )

        # Get PNG bytes of the LangGraph Mermaid diagram
        png_bytes = graph.get_graph().draw_mermaid_png()

        # Save to a file
        with open("sop_agent_graph.png", "wb") as f:
            f.write(png_bytes)

        print("✅ Saved Mermaid PNG as sop_agent_graph.png")

        # Your generic SOP document here
        sop_document = """
        Please perform the following SOP:
        1. Open https://www.accuweather.com/en/in/hyderabad/202190/weather-forecast/202190 in the browser.
        2. Check what is the weather in Hyderabad wait until you get the weather in Hyderabad, if you are not able to fetch the data using elements try to read the html text and get the data.
        3. Run a shell command to list files in the current directory.
        4. Fetch the page title and weather in Hyderabad and create a markdown file with the title and weather in the current directory.
        """

        print("Starting generic multi-agent SOP automation...")

        initial_state = {
            "messages": [{"role": "user", "content": "Start SOP execution."}],
            "sop_document": sop_document
        }

        async for update in graph.astream(initial_state, stream_mode="updates", subgraphs=True):
            print("Update:")
            print(update)

        print("SOP automation complete.")

if __name__ == "__main__":
    asyncio.run(main())
