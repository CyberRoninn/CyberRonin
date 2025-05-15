CyberRonin: Your AI-Powered Linux Co-Pilot (v2.1+)

 

Supercharge your Linux command-line experience with an intelligent AI assistant!

CyberRonin is a Python-based script that integrates with Google Gemini AI (or other LLMs) to provide real-time explanations, suggestions, error troubleshooting, and natural language command translation directly in your terminal. It's designed to help both beginners learn Linux faster and empower experienced users to be more efficient and knowledgeable.


---

Table of Contents

Features

Prerequisites

Installation & Setup

Usage

Configuration

System Prompt for AI

Logging

Future Development

Contributing

License

Disclaimer



---

Features

Intelligent Command Analysis: Get instant explanations of commands you run, their options, and their output.

Natural Language to Command: Describe what you want to do in plain English (e.g., "find all text files modified last week"), and CyberRonin will suggest the appropriate shell command.

Error Troubleshooting: When commands fail, CyberRonin provides AI-powered analysis of error messages and suggests potential fixes.

Contextual Suggestions: Receive suggestions for next logical steps or related commands based on your current activity.

Local Knowledge Base (KB):

Automatically created in ~/.ai_copilot_kb_v2_1/.

AI can suggest useful snippets (command explanations, troubleshooting tips) to save to your local KB.

AI considers information from your local KB when providing assistance.


Rich Terminal Output: Utilizes the rich library for formatted Markdown responses, syntax highlighting, and clear panel displays.

Asynchronous AI Calls: Ensures the UI remains responsive while waiting for AI assistance.

Configurable AI Provider: Primarily designed for Google Gemini, but adaptable for other LLMs.

MOCK Mode: Usable without an API key for testing UI and basic flow (AI responses will be placeholders).

Session Logging: Detailed logs of interactions for review and debugging.

Customizable Prompt: Input prompt styled to mimic a Kali-like terminal.



---

Prerequisites

Python 3.9+

pip (Python package installer)

Access to a supported LLM API (e.g., Google Gemini API key)



---

Installation & Setup

1. Clone the Repository

git clone https://github.com/CyberRoninn/CyberRonin.git
cd CyberRonin


2. Create a Python Virtual Environment (Recommended)

python3 -m venv copilot_env
source copilot_env/bin/activate


3. Install Dependencies

pip install google-generativeai python-dotenv rich


4. Set up API Key

Create a file named .env in the project root.

Add your Google Gemini API key:

GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
# Optional: specify a different Gemini model
# GOOGLE_AI_MODEL="gemini-1.0-pro"


> Note: Keep your API key secure and ensure it's enabled for the Gemini API.




5. Make the Script Executable (Optional)

chmod +x ai_copilot_v2.py




---

Usage

1. Activate Virtual Environment (if used)

source copilot_env/bin/activate


2. Run the Script

python3 ./ai_copilot_v2.py


3. Initial Prompts

The script displays warnings about experimental nature and API costs.

If the API key is missing or invalid, MOCK Mode is offered.

Type understand risks to proceed.



4. Interacting with CyberRonin

Execute Commands: Run any Linux command; CyberRonin then explains or analyzes it.

root@host:~# ls -l /etc

Natural Language Queries: Describe tasks in plain English for command suggestions.

root@host:~# find all log files in /var/log larger than 10MB

AI Prefixes: Use ai?, ??, or explain: for targeted AI assistance.

root@host:~# ai? what are the permissions on /etc/passwd?
root@host:~# explain: how does sudo work?

Accepting Suggestions: Press Enter at the prompt to run the SUGGESTED_NEXT_COMMAND.

Saving KB Snippets: Agree to save KB_SUGGESTION entries for future context.

Exit: Type exit or quit.





---

Configuration

.env File: Contains GOOGLE_API_KEY and optional GOOGLE_AI_MODEL.

Script Globals: Adjust AI_PROVIDER_NAME, KB_DIR_NAME, and LOG_FILE paths in the script.



---

System Prompt for AI

A detailed system prompt within the script drives AI behavior, defining persona, rules, and output formats. Modify the SYSTEM_PROMPT variable to customize responses.


---

Logging

Interactions, prompts, and responses are logged in your Knowledge Base directory, e.g., ~/.ai_copilot_kb_v2_1/copilot_session_v2.x.x.log.


---

Future Development

Support for additional LLM providers (OpenAI, Anthropic).

Advanced KB with semantic search.

Ghost-text autocompletion using prompt_toolkit.

Built-in internet search triggers.

Config file for easier management.

Plugin architecture for custom tools/actions.



---

Contributing

Contributions, suggestions, and bug reports are welcome! Please submit issues or pull requests on GitHub.


---

License

This project is licensed under the MIT License. See LICENSE for details.


---

Disclaimer

CyberRonin is an experimental tool. Always review AI-suggested commands before execution, especially those that modify your system or interact with external resources. Use at your own risk and be mindful of associated API costs.
