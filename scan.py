import json
import sys
import time
import subprocess
import os  
import datetime


VALID_SCANNER_TOOLS = ['wapiti', 'whatweb', 'spiderfoot']

TOOL_OPTIONS = {
    'wapiti': ['full-scan', 'xss-scan', 'sql-injection-scan', 'file-inclusion-scan', 'ssrf-scan'],
    'whatweb': ['global-scan','aggressive-scan'],
    'spiderfoot': ['scan-footprint', 'scan-investigate', 'scan-passive']
}

TOOL_COMMANDS = {
'wapiti': {
    'full-scan': 'wapiti -u {url} -o {output_dir} --detailed-report 2 --color -v 2',
    'xss-scan': 'wapiti -u {url} -m xss -o {output_dir} --detailed-report 2 --color -v 2',
    'sql-injection-scan': 'wapiti -u {url} -m sql,timesql -o {output_dir} --detailed-report 2 --color -v 2',
    'file-inclusion-scan': 'wapiti -u {url} -m file -o {output_dir} --detailed-report 2 --color -v 2',
    'ssrf-scan': 'wapiti -u {url} -m ssrf -o {output_dir} --detailed-report 2 --color -v 2',
},

    'whatweb': {
       'global-scan': 'whatweb {url}',
       'aggressive-scan': 'whatweb -a {url}',
    },
'spiderfoot': {
    'scan-footprint': 'python3 ./spiderfoot/sf.py -s {url} -u footprint -o json > {output_dir}/scan_footprint_{formatted_date}.json',
    'scan-investigate': 'python3 ./spiderfoot/sf.py -s {url} -u investigate -o json > {output_dir}/scan_investigate_{formatted_date}.json',
    'scan-passive': 'python3 ./spiderfoot/sf.py -s {url} -m passive -o json > {output_dir}/scan_passive_{formatted_date}.json',

}

}

def ensure_directories_exist():
    """Ensure the scan-results folder and subfolders (wapiti, whatweb, spiderfoot) exist."""
    base_dir = os.path.join(os.getcwd(), 'scan-results')
    wapiti_dir = os.path.join(base_dir, 'wapiti')
    whatweb_dir = os.path.join(base_dir, 'whatweb')
    spiderfoot_dir = os.path.join(base_dir, 'spiderfoot')

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for folder in [wapiti_dir, whatweb_dir, spiderfoot_dir]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    return base_dir 

def validate_scan_data(scan_data):
    """ Validate scan data before running the scan. """
    print("Validating scan data...", flush=True)

    url = scan_data.get('url')
    if not url:
        return "ERROR: Missing 'url' field."

    if not url.startswith(('http://', 'https://', 'www.')):
        return f"ERROR: Invalid URL format: {url}"

    scanner_tool = scan_data.get('softwareUsed')
    if not scanner_tool:
        return "ERROR: Missing 'softwareUsed' field."

    if scanner_tool not in VALID_SCANNER_TOOLS:
        return f"ERROR: Invalid scanner tool: {scanner_tool}"

    scan_option = scan_data.get('scanOption')
    if scan_option not in TOOL_OPTIONS.get(scanner_tool, []):
        return f"ERROR: Invalid scan option '{scan_option}' for {scanner_tool}."

    print("Validation successful!", flush=True)
    return None 

def generate_scan_command(scan_data, base_dir):
    """ Generate the command based on selected tool and option. """
    
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")

    scanner_tool = scan_data['softwareUsed'] 
    scan_option = scan_data['scanOption'] 
    
    command_template = TOOL_COMMANDS.get(scanner_tool, {}).get(scan_option)
    
    if not command_template:
        return f"ERROR: Command for {scan_option} not found."

    if '{url}' in command_template:
        command = command_template.format(url=scan_data['url'], output_dir=os.path.join(base_dir, scanner_tool),formatted_date=formatted_date
)
    elif '{ipStart}' in command_template and '{ipEnd}' in command_template:
        command = command_template.format(ipStart=scan_data['ipStart'], ipEnd=scan_data['ipEnd'], output_dir=os.path.join(base_dir, scanner_tool),formatted_date=formatted_date
)
    else:
        command = command_template 

    return command

def perform_scan(scan_data):
    """ Simulate a scan process with real-time output. """
    print("Starting scan...", flush=True)
    
    error_message = validate_scan_data(scan_data)
    if error_message:
        print(error_message, flush=True)
        return 

    print(f"Scanning {scan_data['url']} using {scan_data['softwareUsed']} with option {scan_data['scanOption']}...", flush=True)

    base_dir = ensure_directories_exist()

    command = generate_scan_command(scan_data, base_dir)
    if "ERROR" in command:
        print(command, flush=True)
        return
    
    print(f"Generated command: {command}", flush=True)
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for stdout_line in iter(process.stdout.readline, ''):
        if stdout_line:
            print(stdout_line, end='')  

    for stderr_line in iter(process.stderr.readline, ''):
        if stderr_line:
            print(f"ERROR: {stderr_line}", end='')

    process.stdout.close()
    process.stderr.close()
    process.wait()

    if process.returncode != 0:
        print(f"Scan failed with exit code {process.returncode}.", flush=True)
    else:
        print("Scan completed successfully!", flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].strip():
        try:
            scan_data = json.loads(sys.argv[1])  
            perform_scan(scan_data)
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON format.", flush=True)
    else:
        print("ERROR: No scan data provided.", flush=True)
