# Automated Security Scan App
Automated Security Scan App is an automated Python-based scanning tool designed to simplify the process of detecting and identifying security issues in web applications. The app utilizes scanning tools such as Wapiti, WhatWeb, and SpiderFoot, and automates the entire process from installation to scan execution and result visualization.

# Features
- **Automated Scan Setup**: Automatically installs and configures scanning tools like SpiderFoot, WhatWeb, and Wapiti with one click.
- **Multiple Scan Options**: Choose from a variety of scan options tailored to specific vulnerabilities or information gathering needs (e.g., XSS, SQL Injection, Footprint Scan).
- **Real-Time Scan Execution**: Execute scans with a simple interface. Scan results are streamed and displayed live in an embedded iframe.
- **Easy-to-Use Interface**: The user-friendly web interface allows users to quickly start scanning without needing to manually configure tools or enter complex commands.
- **Error Handling**: The app automatically validates inputs and provides helpful error messages if something goes wrong.

## Requirements
- Python >= 3.12.3
- Flask

## Installation

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

    Replace `<repository-url>` with the URL of the repository you want to clone.

2. **Navigate to the project directory:**
    ```bash
    cd <project-directory>
    ```

3. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

4. **Activate the virtual environment:**
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. **Upgrade pip (optional but recommended):**
    - To ensure you're using the latest version of pip, upgrade it:
      ```bash
      pip install --upgrade pip
      ```

6. **Start the Flask development server:**
    ```bash
    python3 main.py
    ```
    By default, the server will run at `http://127.0.0.1:5000`.

