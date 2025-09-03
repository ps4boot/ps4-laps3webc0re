# send_multi_redirect.py
from flask import Flask, render_template_string, request, redirect, url_for
import subprocess

app = Flask(__name__)

FILES = {
    "GoldHEN": "./ELFs/laps3c0re-PS4-11-00.elf",
    "Linux": "./ELFs/laps3c0re-PS4-11-00-linux.elf",
    "HEN": "./ELFs/laps3c0re-PS4-11-00-hen.elf"
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>PS4 OKAge ELF Sender</title>
<style>
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 50px;
}
button {
    font-size: 18px;
    padding: 20px 40px;
    margin: 10px;
    cursor: pointer;
    border-radius: 8px;
    border: 1px solid #333;
    background-color: #4CAF50;
    color: white;
    transition: background-color 0.3s;
}
button:hover {
    background-color: #45a049;
}
#status {
    margin-top: 20px;
    font-weight: bold;
    font-size: 16px;
}
</style>
</head>
<body>
<h1>PS4 OKAge ELF Sender</h1>
{% for name in files %}
    <form action="/send" method="post" style="display:inline-block;">
        <input type="hidden" name="filename" value="{{ files[name] }}">
        <button type="submit">{{ name }}</button>
    </form>
{% endfor %}
<p id="status">{{ status }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE, files=FILES, status="")

@app.route("/send", methods=["POST"])
def send_file():
    filename = request.form.get("filename")
    if filename:
        subprocess.Popen([
            "python", "./mast1c0re-send-file.py",
            "-i", "192.168.1.50",
            "-p", "9045",
            "-f", filename
        ])
    # Nach dem Klick direkt auf die Startseite zurückleiten
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
