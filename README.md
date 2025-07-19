# 🤖 SOP Task Automator with LangChain Agents & MCP Tools 🚀

![LangChain](https://img.shields.io/badge/langchain-v0.1-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-Experimental-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

> 📌 **Highlight**: An intelligent autonomous agent that reads an SOP (Standard Operating Procedure) in plain English and performs the steps — like opening websites, fetching weather, running shell commands, and generating files — all hands-free. 😎

---

## 🧠 What is this?

This project is an **AI-powered task automator** that takes a natural language SOP instruction and **executes it autonomously using LLM agents and Multi-Server MCP adapters**. It seamlessly connects LLMs, browser automation, and system tools — enabling **true autonomous agents** for DevOps, QA, or RPA use cases.

---

## 🌟 Core Features

### ✅ Interprets & Executes Natural Language SOPs
Just describe what you want in plain English — no coding needed! Example:
```text
1. Open a weather website
2. Check weather for Hyderabad 🌧️
3. Run a shell command to list files 📁
4. Create a markdown report 📄
```

### 🧩 Powered by Modular Tools
- 🐚 **ShellTool** — Executes terminal commands.
- 🌐 **Selenium MCP Agent** — Opens and interacts with web pages.
- 🧠 **LangChain Agent** — Coordinates tool usage via LLM reasoning.

### 🔄 Real-time Streaming of Steps
You can **see the agent’s thoughts** and tool usage in real time as it progresses step-by-step through the SOP.

### ✨ Uses GPT-4o-mini
Faster and cheaper than GPT-4, with reliable reasoning and tool selection capabilities.

---

## 🧰 Tech Stack

| Component              | Purpose                                      |
|------------------------|----------------------------------------------|
| `LangChain`            | Agent framework for tool-based reasoning     |
| `ChatOpenAI (GPT-4o-mini)` | Language model driving decisions         |
| `langchain_mcp_adapters` | Bridge to external tool adapters (e.g., Selenium) |
| `ShellTool`            | For shell/terminal command execution         |
| `asyncio`              | For non-blocking concurrent execution        |

---

## 🎬 How It Works (In Plain English)

1. 🏗️ Initializes shell and selenium tools.
2. 🧠 Loads a GPT-4o-mini powered agent with access to these tools.
3. 📄 Feeds in a user-defined SOP as a natural language instruction.
4. ⚙️ Agent reads each instruction, thinks, and selects the right tool.
5. 📡 Executes browser actions and shell commands.
6. 📘 Generates a markdown file with extracted content.
7. 🎯 Done — zero human clicks.

---

## 🌍 Real-World Applications

- 🔍 Automated Web Testing
- 🗃️ Data Gathering Agents
- 📈 RPA for Business Processes
- 📚 SOP Enforcement Bots
- 🧪 QA Environments

---

## 🏁 Run It Locally

> **Requirements**:
> - Python 3.11+
> - Node.js (for MCP-Selenium)
> - OpenAI API Key (set via `OPENAI_API_KEY` env variable)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent
python sop_agent.py
```

---

## 💡 Example Output

```
Starting agent with SOP document...

Step update:
🔧 [Tool used: ShellTool]
🧠 [Thinking: “Need to check the weather on the website...”]
📘 [File created: hyderabad_weather.md]
...

Agent run complete ✅
```

---

## 💥 Why this matters?

This project shows how **AI agents can follow human instructions end-to-end**, bridging the gap between natural language and system automation.

If you're looking to **automate repetitive workflows** or **demonstrate your AI engineering skills** in a tangible way, this is 🔝 portfolio material.

---

## 👨‍💻 Author

Made with ❤️ by [Sekhar Dhana](https://www.linkedin.com/in/sekhar-dhana)  
AI Engineer @ Cigna | Autonomous Agents Enthusiast 🤖

---

## 📜 License

This project is licensed under the MIT License.

---

> ⭐️ If you liked this project, drop a star & share it!  
> Let's bring more autonomy to the world — one agent at a time 🚀