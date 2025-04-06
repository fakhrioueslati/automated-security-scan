import sys
import subprocess
import html
import json
from textwrap import dedent
from flask import Flask, Response, jsonify,render_template,redirect, url_for,request
from verify_tools import verify_tools 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download():
    def g1():
        with subprocess.Popen([sys.executable, '-u', '-c', dedent("""\
            exec(open("download.py").read())""")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as p:
            for line in p.stdout:
                yield f"<code>{html.escape(line.rstrip())}</code><br>\n"
            for line in p.stderr:
                yield f"<code>{html.escape(line.rstrip())}</code><br>\n"
    return Response(g1(), mimetype='text/html')


@app.route('/verify')
def verify():
    def g2():
        output = ""
        with subprocess.Popen([sys.executable, '-u', '-c', dedent("""\
            exec(open("verify_tools.py").read())""")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as p:
            for line in p.stdout:
                output += f"<code>{html.escape(line.rstrip())}</code><br>\n"
            for line in p.stderr:
                output += f"<code>{html.escape(line.rstrip())}</code><br>\n"
        return output
    
    tools_installed, message = verify_tools()

    if tools_installed:
        return jsonify({"redirect": url_for('appscan')})

    return Response(g2(), mimetype='text/html')




@app.route('/app-scan')
def appscan():
    tools_installed, message = verify_tools() 
    
    if not tools_installed:
        return redirect(url_for('home'))
    
    return render_template('scan.html')

@app.route('/scan', methods=['POST'])
def scan():
    tools_installed, message = verify_tools()

    if not tools_installed:
        return Response(f"<h1>Please verify the installation of tools: wapiti, whatweb, spiderfoot. Error: {message}</h1>",
                        status=400, mimetype='text/html')

    scan_data = request.get_json()

    if not scan_data:
        return Response("<h1>No scan data provided</h1>", status=400, mimetype='text/html')

    def g2(scan_data):
        scan_data_json = json.dumps(scan_data)

        process = subprocess.Popen(
            [sys.executable, 'scan.py', scan_data_json],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            yield f"<code>{html.escape(line.rstrip())}</code><br>\n"
        for line in process.stderr:
            yield f"<code style='color:red;'>{html.escape(line.rstrip())}</code><br>\n"

    return Response(g2(scan_data), mimetype='text/html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
