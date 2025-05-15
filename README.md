<div align="center">
  <img src="placeholder_logo.png" alt="CyberRonin Logo" width="150"/> 
  <h1>CyberRonin: Your AI-Powered Linux Co-Pilot</h1>
  <p>
    <strong>Supercharge your Linux command-line experience with an intelligent AI assistant!</strong>
  </p>
  <p>
    <a href="#features">Features</a> •
    <a href="#prerequisites">Prerequisites</a> •
    <a href="#installation--setup">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#future-development">Roadmap</a> •
    <a href="#contributing">Contributing</a> •
    <a href="#disclaimer">Disclaimer</a>
  </p>
  <!-- Optional Badges:
  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
    <img src="https://img.shields.io/github/stars/CyberRoninn/CyberRonin?style=social" alt="GitHub Stars">
  </p>
  -->
</div>

---

CyberRonin (v2.1+) is a Python-based script that integrates with Google's Gemini AI (or other LLMs) to provide real-time explanations, suggestions, error troubleshooting, and natural language command translation directly in your terminal. It's designed to help both beginners learn Linux faster and empower experienced users to be more efficient and knowledgeable.

---

## 🚀 Features

*   🧠 **Intelligent Command Analysis:** Get instant explanations of commands you run, their options, and their output.
*   🗣️ **Natural Language to Command:** Describe what you want to do in plain English (e.g., "find all text files modified last week"), and CyberRonin (via AI) will suggest the appropriate shell command.
*   🛠️ **Error Troubleshooting:** When commands fail, CyberRonin provides AI-powered analysis of error messages and suggests potential fixes.
*   💡 **Contextual Suggestions:** Receive suggestions for next logical steps or related commands based on your current activity.
*   📚 **Local Knowledge Base (KB):**
    *   Automatically created in `~/.ai_copilot_kb_v2_1/` (or similar versioned name).
    *   AI can suggest useful snippets (command explanations, troubleshooting tips) to save to your local KB.
    *   The AI considers information from your local KB when providing assistance.
*   💅 **Rich Terminal Output:** Utilizes the `rich` library for beautifully formatted Markdown responses, syntax highlighting, and clear panel displays.
*   ⚡ **Asynchronous AI Calls:** Ensures the UI remains responsive while waiting for AI assistance.
*   🔧 **Configurable AI Provider:** Primarily designed for Google Gemini, but adaptable for other LLMs.
*   👻 **MOCK Mode:** Usable without an API key for testing UI and basic flow (AI responses will be placeholders).
*   📜 **Session Logging:** Detailed logs of interactions for review and debugging.
*   🎨 **Customizable Prompt:** Input prompt styled to mimic a Kali-like terminal.

---

## 🧰 Prerequisites

*   Python 3.9+
*   `pip` (Python package installer)
*   Access to a supported LLM API (e.g., Google Gemini API key)

---

## 📦 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/CyberRoninn/CyberRonin.git
    cd CyberRonin
    ```
    *(Note: Replace `CyberRoninn/CyberRonin` with your actual GitHub username and repository name if different.)*

2.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python3 -m venv copilot_env
    source copilot_env/bin/activate
    ```
    *(On Windows, use `copilot_env\Scripts\activate`)*

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt 
    ```
    
    Alternatively, install manually:
    ```bash
    pip install google-generativeai python-dotenv rich
    ```

4.  **Set up API Key:**
    *   Create a file named `.env` in the root directory of the project (e.g., inside the `CyberRonin` folder).
    *   Add your Google Gemini API key to it:
        ```env
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY"
        # Optional: Specify a different Gemini model
        # GOOGLE_AI_MODEL="gemini-1.0-pro"
        ```
    *   **IMPORTANT:** Ensure your API key is kept secure and is enabled for the Gemini API. **Do not commit your `.env` file to Git!** Add `.env` to your `.gitignore` file.

5.  **Make the Script Executable:**
    ```bash
    chmod +x ai_copilot_v2.py # Or your main script's filename
    ```

---

## 🛠️ Usage

1.  **Activate Virtual Environment (if used):**
    ```bash
    source copilot_env/bin/activate
    ```

2.  **Run the Script:**
    ```bash
    python3 ./ai_copilot_v2.py # Or your script's filename
    ```
    Or, if executable and in your PATH:
    ```bash
    # ./ai_copilot_v2.py 
    ```

3.  **Initial Prompts:**
    *   The script will display warnings about its experimental nature and API costs.
    *   If your API key is not found or invalid, it will offer to run in "MOCK AI" mode.

4.  **Interacting with CyberRonin:**

    *   **Type Linux Commands:** Execute commands as you normally would. After execution, the AI will provide analysis and suggestions.
        ```bash
        root@localhost:~# ls -l /etc
        ```
    *   **Ask Natural Language Questions:** Type your task description in plain English. The AI will attempt to translate it into a shell command for your approval.
        ```bash
        root@localhost:~# find all log files in /var/log larger than 10MB
        ```
    *   **Explicit AI Queries:** Use prefixes like `ai?`, `??`, `explain:` to ask specific questions about the last command or general Linux topics.
        ```bash
        root@localhost:~# ai? what are the permissions on that file?
        root@localhost:~# explain: how does sudo work?
        ```
    *   **Accepting AI Suggested Next Command:** If the AI suggests a command with `SUGGESTED_NEXT_COMMAND:`, it will appear in your next prompt like `(AI: <suggested_command>)`. Simply pressing Enter without typing anything else will execute that suggested command.
    *   **Saving to Knowledge Base:** If the AI includes `KB_SUGGESTION:`, you'll be prompted to save it to your local KB.
    *   **Exiting:** Type `exit` or `quit`.

---

## ⚙️ Configuration

*   **`.env` file:** For `GOOGLE_API_KEY` and `GOOGLE_AI_MODEL`. Located in the project root.
*   **Script Globals:** Some settings like `AI_PROVIDER_NAME`, `KB_DIR_NAME`, `LOG_FILE` paths are defined as global variables within the script and can be adjusted there if needed. (A dedicated config file is planned for future development).

---

## 🧠 System Prompt for AI

The behavior of the AI is heavily guided by a detailed system prompt embedded within the script (`SYSTEM_PROMPT` variable). This prompt defines its persona ("CyberRonin"), operational rules, ethical guidelines, and expected output format. Modifying this prompt is the primary way to tune the AI's assistance.

---

## 📝 Logging

Session activity, AI prompts (snippets), and AI responses (snippets) are logged to a file within your Knowledge Base directory (e.g., `~/.ai_copilot_kb_v2_1/copilot_session_v2.x.x.log`). This log is invaluable for debugging, reviewing interactions, and understanding the AI's decision-making process.

---

## 🔮 Future Development

*   Support for more LLM providers (OpenAI, Anthropic, local models).
*   Advanced Knowledge Base with semantic search capabilities.
*   True "ghost text" autocompletion for AI suggestions using `prompt_toolkit`.
*   Implementation of the `SEARCH_INTERNET:` directive for the AI.
*   Dedicated configuration file (e.g., YAML or INI) for easier settings management.
*   A basic plugin system for user-defined tools or actions.
*   Enhanced context management for longer conversations.

---

## 🤝 Contributing

This project is currently in an experimental phase. Contributions, suggestions, and bug reports are welcome! Please feel free to:
*   Open an issue for bugs or feature requests.
*   Fork the repository and submit a pull request.

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

CyberRonin (AI Linux Co-Pilot) is an experimental tool. **Always review AI-suggested commands before execution**, especially those that modify your system, install software, or interact with external resources. The accuracy and safety of AI-generated commands cannot be guaranteed.

The developers and contributors are not responsible for any damage, data loss, or unintended consequences resulting from the use of this script. **Use at your own risk.** Be mindful of API costs associated with your chosen LLM provider.