#!/usr/bin/env python3
# ai_linux_copilot.py

import os
import sys
import json
import re
import subprocess
import readline
import time
from pathlib import Path
import traceback

try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv not found. Run: pip install python-dotenv")
    sys.exit(1)

try:
    import google.generativeai as genai
except ImportError:
    print("google-generativeai not found. Run: pip install google-generativeai")
    sys.exit(1)

# --- Color Definitions ---
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
NC = '\033[0m'

# --- Configuration ---
KB_DIR_NAME = ".ai_linux_copilot_kb"
KB_PATH = Path.home() / KB_DIR_NAME
LOG_FILE = KB_PATH / "copilot_session.log"
AI_RESULTS_HISTORY = KB_PATH / "ai_results_history.json"

# Load API Key
dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AI_MODEL_NAME = os.getenv("GOOGLE_AI_MODEL", "gemini-1.5-flash-latest")
AI_RESPONSE_COOLDOWN = 2  # Seconds between AI calls to prevent flooding

# Global state variables
last_ai_call_time = 0
last_suggested_command = ""
ai_throttled = False

# --- Helper Functions ---
def log_message(message, to_file=True, to_console=True, level="INFO", color=NC):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} [{level}] {message}"
    if to_console:
        print(f"{color}{log_entry}{NC}")
    if to_file:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(log_entry + "\n")

def ensure_kb_exists():
    KB_PATH.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)
    # Load or initialize AI results history
    if AI_RESULTS_HISTORY.exists():
        with open(AI_RESULTS_HISTORY, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
        with open(AI_RESULTS_HISTORY, 'w') as f:
            json.dump(data, f)
    log_message("Knowledge Base directory ensured.", color=GREEN)

def save_to_kb(filename, content, category="general"):
    category_path = KB_PATH / category
    category_path.mkdir(parents=True, exist_ok=True)
    file_path = category_path / filename
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(content)
    log_message(f"Saved '{filename}' to KB under '{category}'.", color=GREEN)

def search_kb(query_terms, category="general"):
    category_path = KB_PATH / category
    results = []
    if category_path.exists():
        for item in category_path.iterdir():
            if item.is_file():
                try:
                    content = item.read_text(encoding='utf-8')
                    if any(term.lower() in content.lower() for term in query_terms):
                        results.append({"filename": item.name, "content_snippet": content[:200] + "..."})
                except Exception as e:
                    log_message(f"Error reading KB file {item.name}: {e}", level="ERROR", color=RED)
    return results

def save_ai_response_to_history(command, ai_response):
    entry = {
        "command": command,
        "response": ai_response,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        with open(AI_RESULTS_HISTORY, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(entry)
    with open(AI_RESULTS_HISTORY, 'w') as f:
        json.dump(data, f, indent=2)

# --- AI Interaction ---
def get_ai_assistance(command_history, current_command, command_output, error_output, user_question=None):
    global last_ai_call_time, ai_throttled

    current_time = time.time()
    if current_time - last_ai_call_time < AI_RESPONSE_COOLDOWN:
        ai_throttled = True
        return "AI on cooldown. Wait a moment before requesting help again."

    if not GOOGLE_API_KEY:
        log_message("GOOGLE_API_KEY not found. AI assistance disabled.", level="ERROR", color=RED)
        return "AI Error: API Key not configured."

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(AI_MODEL_NAME)
    except Exception as e:
        log_message(f"Error configuring Gemini AI: {e}", level="ERROR", color=RED)
        return f"AI Configuration Error: {e}"

    # Construct the prompt for the AI
    prompt_parts = [
        "You are an AI Linux Co-Pilot. Your goal is to help the user understand Linux commands and their output, suggest improvements, and provide learning assistance.",
        "--- Recent Command History (if any) ---"
    ]
    for hist_cmd, hist_out, hist_err in command_history[-3:]:
        prompt_parts.append(f"Cmd: {hist_cmd}\nOutput: {hist_out if hist_out else '(no stdout)'}\nError: {hist_err if hist_err else '(no stderr)'}\n---")

    prompt_parts.append(f"--- Current Interaction ---")
    prompt_parts.append(f"User executed: `{current_command}`")
    if command_output: prompt_parts.append(f"STDOUT:\n```\n{command_output.strip()}\n```")
    if error_output: prompt_parts.append(f"STDERR:\n```\n{error_output.strip()}\n```")
    if user_question: prompt_parts.append(f"User's specific question: \"{user_question}\"")

    # Search local KB first for relevant info
    kb_query_terms = current_command.split() + (error_output.split() if error_output else [])
    kb_results = search_kb(kb_query_terms)
    if kb_results:
        prompt_parts.append("\n--- Relevant Information from Local Knowledge Base ---")
        for res in kb_results[:2]:
            prompt_parts.append(f"File: {res['filename']}\nSnippet: {res['content_snippet']}\n---")
    
    prompt_parts.append("\n--- Your Task ---")
    prompt_parts.append(
        "1. Briefly explain the executed command (`" + current_command + "`). Focus on the options used if any."
        "2. Interpret the STDOUT and STDERR. Highlight key information or error causes."
        "3. Suggest potential next steps or related commands the user might find useful."
        "4. If there was an error, suggest common fixes or troubleshooting steps. Check the KB snippets first."
        "5. If the user asked a question, answer it directly in context."
        "6. If relevant, mention if a more efficient command or alternative tool exists for the task."
        "7. OPTIONAL: If you have high confidence and the information is not sensitive, suggest a useful snippet or explanation that could be saved to the local Knowledge Base. Prefix it with 'KB_SUGGESTION:'. The user will confirm saving."
        "8. Keep your response concise, helpful, and easy to understand. Use Markdown for formatting."
        "9. If you need to search the internet for up-to-date information (e.g., man pages, specific error codes), indicate this by starting your response with `SEARCH_INTERNET: [search query]`. The wrapper script will handle the search and provide results back to you in a subsequent call."
    )
    
    full_prompt = "\n".join(prompt_parts)
    log_message(f"Sending prompt to AI (length {len(full_prompt)}):\n{full_prompt[:500]}...", color=CYAN, to_console=False)

    try:
        response = model.generate_content(full_prompt)
        ai_text_response = response.text
        log_message(f"AI Raw Response:\n{ai_text_response}", color=CYAN, to_console=False)
        
        # Save AI response to history
        save_ai_response_to_history(current_command, ai_text_response)
        
        last_ai_call_time = current_time
        ai_throttled = False
        return ai_text_response
    except Exception as e:
        log_message(f"Error during AI content generation: {e}", level="ERROR", color=RED)
        last_ai_call_time = current_time
        ai_throttled = False
        return f"AI Generation Error: {e}"

# --- Shell Interaction ---
def execute_command_in_subprocess(command_str, current_dir):
    log_message(f"Executing: {command_str} in {current_dir}", color=YELLOW)
    try:
        if command_str.strip().startswith("cd "):
            try:
                new_dir_str = command_str.strip()[3:].strip()
                if new_dir_str.startswith("~"):
                    new_dir_str = str(Path.home()) + new_dir_str[1:]
                
                target_dir = Path(current_dir) / new_dir_str
                if not target_dir.is_absolute():
                    target_dir = Path(new_dir_str)

                os.chdir(target_dir.resolve())
                return os.getcwd(), "", ""
            except FileNotFoundError:
                return current_dir, "", f"cd: no such file or directory: {new_dir_str}"
            except Exception as e:
                return current_dir, "", f"cd: error changing directory: {e}"

        process = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
            cwd=current_dir,
            check=False
        )
        return current_dir, process.stdout, process.stderr
    except Exception as e:
        log_message(f"Error executing command '{command_str}': {e}", level="ERROR", color=RED)
        return current_dir, "", str(e)

# --- Main Loop ---
def main():
    ensure_kb_exists()
    log_message("AI Linux Co-Pilot V1.0 Started", color=GREEN, to_file=True, to_console=True)
    print(f"{MAGENTA}Welcome to AI Linux Co-Pilot! Type 'exit' or 'quit' to leave.{NC}")
    print(f"{CYAN}Special commands:")
    print(" - ai? <question>: Ask AI about previous command or general Linux question")
    print(" - help: Show available commands")
    print(" - history: Show recent command history")
    print(" - kb <search term>: Search knowledge base")
    print(" - settings: Show current settings{NC}")

    command_history = []
    current_working_dir = os.getcwd()
    last_ai_response = None

    while True:
        try:
            # Construct prompt with current working directory
            user_prompt_display = f"{BLUE}{Path(current_working_dir).name}{NC}$ "
            if os.geteuid() == 0:
                user_prompt_display = f"{RED}{Path(current_working_dir).name}{NC}# "

            user_command = input(user_prompt_display).strip()

            if user_command.lower() in ["exit", "quit"]:
                break
            if not user_command:
                continue

            # Handle special commands
            if user_command.lower().startswith("ai?"):
                question = user_command[4:].strip()
                if not command_history:
                    print(f"{YELLOW}No previous command to ask about. Ask a general Linux question or run a command first.{NC}")
                    ai_response_text = get_ai_assistance([], "", "", "", user_question=question)
                else:
                    last_cmd, last_stdout, last_stderr = command_history[-1]
                    ai_response_text = get_ai_assistance(
                        command_history[:-1], last_cmd, last_stdout, last_stderr, user_question=question
                    )
                print(f"\n{CYAN}--- AI Co-Pilot ---\n{ai_response_text}{NC}\n")
                last_ai_response = ai_response_text
                continue

            if user_command.lower() == "help":
                print(f"{CYAN}Available commands:")
                print(" - ai? <question>: Ask AI about previous command or general Linux question")
                print(" - history: Show recent command history")
                print(" - kb <search term>: Search knowledge base")
                print(" - settings: Show current settings")
                print(" - undo: Undo last command (if possible)")
                print(" - clear: Clear screen")
                print(" - exit/quit: Exit the co-pilot{NC}")
                continue

            if user_command.lower() == "history":
                if command_history:
                    print(f"{CYAN}Recent Commands:")
                    for i, (cmd, _, _) in enumerate(command_history[-5:]):
                        print(f" {i+1}. {cmd}")
                    print(f"{NC}")
                else:
                    print(f"{YELLOW}No command history yet.{NC}")
                continue

            if user_command.lower().startswith("kb "):
                search_term = user_command[3:].strip()
                if not search_term:
                    print(f"{YELLOW}Please provide a search term for the knowledge base.{NC}")
                    continue
                results = search_kb(search_term.split())
                if results:
                    print(f"{CYAN}Knowledge Base Results:")
                    for res in results:
                        print(f" - {res['filename']}: {res['content_snippet']}")
                    print(f"{NC}")
                else:
                    print(f"{YELLOW}No results found in knowledge base.{NC}")
                continue

            if user_command.lower() == "settings":
                print(f"{CYAN}Current Settings:")
                print(f" - AI Model: {AI_MODEL_NAME}")
                print(f" - API Key Configured: {'Yes' if GOOGLE_API_KEY else 'No'}")
                print(f" - Knowledge Base Location: {KB_PATH}")
                print(f" - AI Response Cooldown: {AI_RESPONSE_COOLDOWN} seconds{NC}")
                continue

            if user_command.lower() == "undo":
                if command_history:
                    # Simple undo by removing last command from history
                    removed_cmd = command_history.pop()
                    print(f"{CYAN}Undid command: {removed_cmd[0]}{NC}")
                else:
                    print(f"{YELLOW}No commands to undo.{NC}")
                continue

            if user_command.lower() == "clear":
                os.system('clear' if os.name == 'posix' else 'cls')
                continue

            # Execute command
            previous_cwd = current_working_dir
            current_working_dir, cmd_stdout, cmd_stderr = execute_command_in_subprocess(user_command, current_working_dir)
            
            if cmd_stdout: print(f"{GREEN}Output:\n{cmd_stdout.strip()}{NC}")
            if cmd_stderr: print(f"{RED}Error Output:\n{cmd_stderr.strip()}{NC}")

            command_history.append((user_command, cmd_stdout, cmd_stderr))

            # Get AI assistance with cooldown check
            if GOOGLE_API_KEY and not ai_throttled:
                print(f"{MAGENTA}Co-Pilot is thinking...{NC}")
                ai_response_text = get_ai_assistance(command_history[:-1], user_command, cmd_stdout, cmd_stderr)
                print(f"\n{CYAN}--- AI Co-Pilot ---\n{ai_response_text}{NC}\n")

                # Handle KB suggestions
                kb_suggestion_match = re.search(r"KB_SUGGESTION:\s*([\s\S]+)", ai_response_text, re.IGNORECASE)
                if kb_suggestion_match:
                    suggestion_text = kb_suggestion_match.group(1).strip()
                    if input(f"{YELLOW}AI suggests saving this to Knowledge Base. Save? (y/n): {NC}").lower() == 'y':
                        kb_filename_base = re.sub(r'\W+', '_', user_command.split()[0])
                        kb_filename = f"{kb_filename_base}_{int(time.time())}.md"
                        save_to_kb(kb_filename, f"# Command: {user_command}\n\n{suggestion_text}", category="ai_suggestions")

            elif ai_throttled:
                print(f"{YELLOW}AI is on cooldown. Wait a moment before requesting help again.{NC}")

        except KeyboardInterrupt:
            print("\nExiting Co-Pilot...")
            break
        except EOFError:
             print("\nExiting Co-Pilot...")
             break
        except Exception as e:
            log_message(f"Error in main loop: {e}", level="CRITICAL", color=RED)
            traceback.print_exc()

    log_message("AI Linux Co-Pilot Session Ended", color=GREEN)

if __name__ == "__main__":
    if not GOOGLE_API_KEY:
        print(f"{YELLOW}WARNING: GOOGLE_API_KEY not found in .env or environment variables.{NC}")
        print(f"{YELLOW}AI assistance will be disabled. The script will function as a basic shell wrapper.{NC}")
        if input(f"{YELLOW}Continue without AI assistance? (y/n): {NC}").lower() != 'y':
            sys.exit(0)
    main()
