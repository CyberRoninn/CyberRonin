<div align="center">
  <!-- Replace placeholder_logo.png with your actual logo and uncomment the line below -->
  <!-- <img src="placeholder_logo.png" alt="CyberRonin Logo" width="150"/> -->
  <h1>CyberRonin: Your AI-Powered Linux Co-Pilot</h1>
  <p>
    <strong>Supercharge your Linux command-line experience with an intelligent AI assistant!</strong>
  </p>
  <p>
    <a href="#-demo">Demo</a> •
    <a href="#features">Features</a> •
    <a href="#prerequisites">Prerequisites</a> •
    <a href="#installation--setup">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#future-development">Roadmap</a> •
    <a href="#contributing">Contributing</a> •
    <a href="#license">License</a> •
    <a href="#disclaimer">Disclaimer</a>
  </p>
  <!-- Optional Badges:
  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
    <img src="https://img.shields.io/github/stars/YOUR_USERNAME/YOUR_REPONAME?style=social" alt="GitHub Stars">
  </p>
  -->
</div>

---

CyberRonin (v2.1+) is a Python-based script that integrates with Google's Gemini AI (or other LLMs) to provide real-time explanations, suggestions, error troubleshooting, and natural language command translation directly in your terminal. It's designed to help both beginners learn Linux faster and empower experienced users to be more efficient and knowledgeable.

---

## 🎥 Demo

See CyberRonin in action!

[![Watch the CyberRonin Demo on YouTube](https://img.youtube.com/vi/C1ecfb2Xyzg/hqdefault.jpg)](https://youtube.com/shorts/C1ecfb2Xyzg?si=GUOG5Sxie45Vo7UX)
<p align="center"><em>Click the image above to watch the demo on YouTube Shorts.</em></p>

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
    git clone https://github.com/YOUR_USERNAME/YOUR_REPONAME.git 
    cd YOUR_REPONAME
    ```
    *(Ensure you update `YOUR_USERNAME/YOUR_REPONAME`.)*

2.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python3 -m venv copilot_env
    source copilot_env/bin/activate
    ```
    *(On Windows, use `copilot_env\Scripts\activate`)*

3.  **Install Dependencies:**
    *(Ensure a `requirements.txt` file is present in the repository)*
    ```bash
    pip install -r requirements.txt 
    ```

4.  **Set up API Key:**
    *   Create a file named `.env` in the root directory of the project.
    *   Add your Google Gemini API key to it:
        ```env
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY"
        # Optional: Specify a different Gemini model
        # GOOGLE_AI_MODEL="gemini-1.0-pro"
        ```
    *   **IMPORTANT:** Ensure your API key is kept secure and is enabled for the Gemini API. Add `.env` to your `.gitignore` file.

5.  **Make the Script Executable (Optional):**
    ```bash
    chmod +x ai_copilot_v2.py # Replace with your main script's filename
    ```

---

## 🛠️ Usage

1.  **Activate Virtual Environment (if used):**
    ```bash
    source copilot_env/bin/activate
    ```

2.  **Run the Script:**
    ```bash
    python3 ./ai_copilot_v2.py # Replace with your main script's filename
    ```

3.  **Initial Prompts:**
    *   The script will display warnings about its experimental nature and API costs.
    *   If your API key is not found or invalid, it will offer to run in "MOCK AI" mode.
    *   You'll be asked to type `understand risks` to proceed.

4.  **Interacting with CyberRonin:**
    *   **Type Linux Commands:**
        ```bash
        root@localhost:~# ls -l /etc
        ```
    *   **Ask Natural Language Questions:**
        ```bash
        root@localhost:~# find all log files in /var/log larger than 10MB
        ```
    *   **Explicit AI Queries:** (Use prefixes `ai?`, `??`, `explain:`)
        ```bash
        root@localhost:~# ai? what are the permissions on that file?
        ```
    *   **Accepting AI Suggested Next Command:** Press Enter if a suggestion appears like `(AI: <suggested_command>)`.
    *   **Saving to Knowledge Base:** Confirm with 'y' when prompted after `KB_SUGGESTION:`.
    *   **Exiting:** Type `exit` or `quit`.

---

## ⚙️ Configuration

*   **`.env` file:** For `GOOGLE_API_KEY` and `GOOGLE_AI_MODEL`.
*   **Script Globals:** For `AI_PROVIDER_NAME`, `KB_DIR_NAME`, etc. (Config file planned).

---

## 🧠 System Prompt for AI

The AI's behavior is guided by the `SYSTEM_PROMPT` variable in the script. Modify this to tune AI assistance.

---

## 📝 Logging

Session logs are in `~/.ai_copilot_kb_v2_1/copilot_session_v2.x.x.log` (versioned).

---

## 🔮 Future Development

*   Support for more LLMs.
*   Advanced KB with semantic search.
*   True "ghost text" autocompletion (`prompt_toolkit`).
*   Internet search capability.
*   Dedicated configuration file.
*   Plugin system.

---

## 🤝 Contributing

This project is experimental. Contributions, suggestions, and bug reports are welcome!
*   Open an issue for bugs or feature requests.
*   Fork the repository and submit a pull request.
*(Consider adding a `CONTRIBUTING.md` file.)*

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Ensure you add a `LICENSE` file.)*

---

## ⚠️ Disclaimer

CyberRonin (AI Linux Co-Pilot) is an experimental tool. **Always review AI-suggested commands before execution**, especially those that modify your system, install software, or interact with external resources. The accuracy and safety of AI-generated commands cannot be guaranteed.

The developers and contributors are not responsible for any damage, data loss, or unintended consequences resulting from the use of this script. **Use at your own risk.** Be mindful of API costs associated with your chosen LLM provider.