# CyberRonin: Your AI-Powered Linux Co-Pilot (v2.1+)

**Supercharge your Linux command-line experience with an intelligent AI assistant!**

CyberRonin is a Python-based script that integrates with Google's Gemini AI (or other LLMs) to provide real-time explanations, suggestions, error troubleshooting, and natural language command translation directly in your terminal. It's designed to help both beginners learn Linux faster and empower experienced users to be more efficient and knowledgeable.

## Features

*   **Intelligent Command Analysis:** Get instant explanations of commands you run, their options, and their output.
*   **Natural Language to Command:** Describe what you want to do in plain English (e.g., "find all text files modified last week"), and CyberRonin (via AI) will suggest the appropriate shell command.
*   **Error Troubleshooting:** When commands fail, CyberRonin provides AI-powered analysis of error messages and suggests potential fixes.
*   **Contextual Suggestions:** Receive suggestions for next logical steps or related commands based on your current activity.
*   **Local Knowledge Base (KB):**
    *   Automatically created in `~/.ai_copilot_kb_v2_1/` (or similar versioned name).
    *   AI can suggest useful snippets (command explanations, troubleshooting tips) to save to your local KB.
    *   The AI considers information from your local KB when providing assistance.
*   **Rich Terminal Output:** Utilizes the `rich` library for beautifully formatted Markdown responses, syntax highlighting, and clear panel displays.
*   **Asynchronous AI Calls:** Ensures the UI remains responsive while waiting for AI assistance.
*   **Configurable AI Provider:** Primarily designed for Google Gemini, but adaptable for other LLMs.
*   **MOCK Mode:** Usable without an API key for testing UI and basic flow (AI responses will be placeholders).
*   **Session Logging:** Detailed logs of interactions for review and debugging.
*   **Customizable Prompt:** Input prompt styled to mimic a Kali-like terminal.

## Prerequisites

*   Python 3.9+
*   `pip` (Python package installer)
*   Access to a supported LLM API (e.g., Google Gemini API key)

## Installation & Setup

1.  **Clone the Repository (or download the script):**
    ```bash
    # If it were a git repo:
    # git clone https://github.com/elpazzo21/CyberRonin.git
    # cd  ai_copilot_v2.py
    # For now, just save the script (e.g., ai_copilot_v2.1_env_debug.py) to a directory.
    ```

2.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python3 -m venv copilot_env
    source copilot_env/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install google-generativeai python-dotenv rich
    ```

4.  **Set up API Key:**
    *   Create a file named `.env` in the same directory as the script.
    *   Add your Google Gemini API key to it:
        ```env
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY"
        # Optional: Specify a different Gemini model
        # GOOGLE_AI_MODEL="gemini-1.0-pro"
        ```
    *   **IMPORTANT:** Ensure your API key is kept secure and is enabled for the Gemini API.

5.  **Make the Script Executable (Optional):**
    ```bash
    chmod +x ai_copilot_v2.py # Or your script's filename
    ```

## Usage

1.  **Activate Virtual Environment (if used):**
    ```bash
    source copilot_env/bin/activate
    ```

2.  **Run the Script:**
    ```bash
    python3 ./ai_copilot_v2.py # Or your script's filename
    ```

3.  **Initial Prompts:**
    *   The script will display warnings about its experimental nature and API costs.
    *   If your API key is not found or invalid, it will offer to run in "MOCK AI" mode.
    *   You'll be asked to type `understand risks` to proceed.

4.  **Interacting with CyberRonin:**
    *   **Type Linux Commands:** Execute commands as you normally would. After execution, the AI will provide analysis and suggestions.
        ```
        root@localhost:~# ls -l /etc
        ```
    *   **Ask Natural Language Questions:** Type your task description in plain English. The AI will attempt to translate it into a shell command for your approval.
        ```
        root@localhost:~# find all log files in /var/log larger than 10MB
        ```
    *   **Explicit AI Queries:** Use prefixes like `ai?`, `??`, `explain:` to ask specific questions about the last command or general Linux topics.
        ```
        root@localhost:~# ai? what are the permissions on that file?
        root@localhost:~# explain: how does sudo work?
        ```
    *   **Accepting AI Suggested Next Command:** If the AI suggests a command with `SUGGESTED_NEXT_COMMAND:`, it will appear in your next prompt like `(AI: <suggested_command>)`. Simply pressing Enter without typing anything else will execute that suggested command.
    *   **Saving to Knowledge Base:** If the AI includes `KB_SUGGESTION:`, you'll be prompted to save it to your local KB.
    *   **Exiting:** Type `exit` or `quit`.

## Configuration

*   **`.env` file:** For `GOOGLE_API_KEY` and `GOOGLE_AI_MODEL`.
*   **Script Globals:** `AI_PROVIDER_NAME` can be changed in the script (though currently only Google is fully implemented). `KB_DIR_NAME`, `LOG_FILE` paths can also be adjusted.

## System Prompt for AI

The behavior of the AI is heavily guided by a detailed system prompt embedded within the script. This prompt defines its persona, rules, and expected output format. Modifying this prompt can change how the AI assists. (Refer to the `SYSTEM_PROMPT` variable in the script).

## Logging

Session activity, AI prompts, and AI responses are logged to a file within your Knowledge Base directory (e.g., `~/.ai_copilot_kb_v2_1/copilot_session_v2.x.x.log`). This is useful for debugging and reviewing interactions.

## Future Development

(See Section IV below for more details)
*   Support for more LLM providers (OpenAI, Anthropic).
*   Advanced Knowledge Base with semantic search.
*   True "ghost text" autocompletion using `prompt_toolkit`.
*   Internet search capability triggered by AI.
*   Configuration file for easier settings management.
*   Plugin system for custom tools/actions.

## Contributing

This project is currently in an experimental phase. Contributions, suggestions, and bug reports are welcome! (If this were a public repo, provide contribution guidelines here).

## Disclaimer

CyberRonin (AI Linux Co-Pilot) is an experimental tool. Always review AI-suggested commands before execution, especially those that modify your system or interact with external resources. The developers are not responsible for any damage or unintended consequences resulting from the use of this script. Use at your own risk. Be mindful of API costs associated with the LLM provider.
