import subprocess
import sys
import html
from pathlib import Path
import shutil

CURRENT_DIR = Path.cwd()
SPIDERFOOT_DIR = CURRENT_DIR / "spiderfoot"
SPIDERFOOT_SCRIPT = SPIDERFOOT_DIR / "sf.py"

def check_tools():
    missing_tools = []

    if not SPIDERFOOT_DIR.exists() or not SPIDERFOOT_SCRIPT.exists():
        missing_tools.append("spiderfoot")

    if not shutil.which("wapiti"):
        missing_tools.append("wapiti")

    if not shutil.which("whatweb"):
        missing_tools.append("whatweb")

    return missing_tools

def clear_spiderfoot_directory():
    if SPIDERFOOT_DIR.exists():
        shutil.rmtree(SPIDERFOOT_DIR)

def verify_tools():
    missing_tools = check_tools()

    if missing_tools:
        error_message = f"The following tools are missing or not found: {', '.join(missing_tools)}. Please click the install button."
        return False, error_message

    return True, "All tools are installed."

def execute_verification():
    tools_installed, message = verify_tools()

    if not tools_installed:
        print(f"{html.escape(message)}")
        return message

    clear_spiderfoot_directory()
    print("All tools are installed correctly.")
    return message

if __name__ == "__main__":
    execute_verification()
