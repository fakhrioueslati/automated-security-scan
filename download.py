import os
import subprocess
import shutil
from pathlib import Path

current_dir = Path.cwd()
COMMANDS_DIR = current_dir / "commands"

SPIDERFOOT_DIR = current_dir / "spiderfoot"

def load_commands():
    commands = {}
    command_files = {
        "wapiti": COMMANDS_DIR / "cmdwapiti.txt",
        "whatweb": COMMANDS_DIR / "cmdwhatweb.txt",
        "spiderfoot": COMMANDS_DIR / "cmdspiderfoot.txt"
    }

    for tool, file_path in command_files.items():
        if file_path.exists():
            with open(file_path, 'r') as f:
                commands[tool] = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            print(f"Warning: Command file for {tool} not found: {file_path}")

    return commands

def create_directories():
    directories = [SPIDERFOOT_DIR] 
    for directory in directories:
        if directory.exists():
            print(f"Clearing contents of existing directory: {directory}")
            for item in directory.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)  
                else:
                    item.unlink()  
        else:
            print(f"Created directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)

def get_tool_directory(tool):
    return {
        "spiderfoot": SPIDERFOOT_DIR
    }.get(tool, None)

def execute_commands(commands_dict):
    for tool in ["wapiti", "whatweb"]:
        if tool in commands_dict:
            print(f"Executing {tool} setup commands:")
            for command in commands_dict[tool]:
                print(f"Running: {command}")
                subprocess.run(command, shell=True, check=True)

    for tool, commands in commands_dict.items():
        if tool == "spiderfoot":
            tool_dir = get_tool_directory(tool)
            if not tool_dir:
                print(f"Tool directory for {tool} not found.")
                continue

            os.chdir(tool_dir)
            print(f"Changed directory to {os.getcwd()}")

            for index, command in enumerate(commands):
                print(f"Executing command {index + 1}/{len(commands)} for {tool}: {command}")
                try:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    for stdout_line in process.stdout:
                        print(stdout_line, end="", flush=True)  

                    for stderr_line in process.stderr:
                        print(stderr_line, end="", flush=True) 

                    process.wait()

                    if process.returncode != 0:
                        print(f"Error executing command: {command}")
                except subprocess.CalledProcessError as e:
                    print(f"Error executing command: {e}")

def main():
    create_directories()
    commands_dict = load_commands()
    if not commands_dict:
        print("No commands to execute. Exiting.")
        return

    execute_commands(commands_dict)
    print("\nFinished setting up the tools. You are now ready to start.")
    print("Click the 'Start' button to begin the scan.")

if __name__ == "__main__":
    main()
