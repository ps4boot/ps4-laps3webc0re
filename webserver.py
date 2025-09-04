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
        margin: 0;
        padding: 0;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: url('/static/bg.jpg') no-repeat center center fixed;
        background-size: cover;
        color: white;
        text-shadow: 0 0 8px rgba(0,0,0,0.7);
    }
    h1 {
        margin-bottom: 60px;
        font-size: 3.5em;
        letter-spacing: 2px;
    }
    .button-container {
        display: flex;
        gap: 60px;
        flex-wrap: wrap;
        justify-content: center;
    }
    form {
        display: inline-block;
    }
    .icon-button {
        width: 210px;   /* doppelte Größe */
        height: 210px;  /* doppelte Größe */
        border: none;
        border-radius: 25px;
        background: rgba(0,0,255,0.15);
        backdrop-filter: blur(8px);
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        padding: 0;
        position: relative;
        overflow: hidden;
    }
    .icon-button img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 25px;
    }
    .icon-button:hover {
        transform: scale(1.1) rotate(-2deg);
        box-shadow: 0 0 35px rgba(0,0,0,0.9);
    }
    .label {
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        color: yellow;
        font-size: 1.4em;
        text-shadow: 0 0 6px black;
        opacity: 0;
        transition: opacity 0.3s;
        font-weight: bold;
    }
    .icon-button:hover .label {
        opacity: 1;
    }
    #status {
        margin-top: 40px;
        font-size: 1.4em;
        font-weight: bold;
    }
</style>
</head>
<body>
<h1>PS4 OKAge ELF Sender</h1>
<div class="button-container">
    {% for name in files %}
        <form action="/send" method="post">
            <input type="hidden" name="filename" value="{{ files[name] }}">
            <button type="submit" class="icon-button">
                {% if name == "GoldHEN" %}
                    <img src="/static/goldhen.png" alt="GoldHEN">
                {% elif name == "HEN" %}
                    <img src="/static/hen.png" alt="HEN">
                {% elif name == "Linux" %}
                    <img src="/static/linux.png" alt="Linux">
                {% else %}
                    <img src="https://via.placeholder.com/300?text={{ name }}" alt="{{ name }}">
                {% endif %}
                <div class="label">{{ name }}</div>
            </button>
        </form>
    {% endfor %}
</div>
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
