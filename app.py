from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from datetime import date
import csv
import socket

app = Flask(__name__)
BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "nippo.csv"

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", today=date.today().isoformat())

@app.route("/submit", methods=["POST"])
def submit():
    DATA.parent.mkdir(exist_ok=True)
    new_file = not DATA.exists()
    row = [
        request.form.get("work_date", ""),
        request.form.get("weather", ""),
        request.form.get("company", ""),
        request.form.get("work", ""),
        request.form.get("people", ""),
        request.form.get("note", ""),
    ]
    with DATA.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["日付", "天気", "業者名", "作業内容", "人数", "備考"])
        w.writerow(row)
    return redirect(url_for("done"))

@app.route("/done")
def done():
    return render_template("done.html")

if __name__ == "__main__":
    ip = local_ip()
    print()
    print("==============================================")
    print(" Construction Daily Report Test")
    print("==============================================")
    print(" PC   : http://127.0.0.1:8000")
    print(f" iPad : http://{ip}:8000")
    print("==============================================")
    print()
    app.run(host="0.0.0.0", port=8000, debug=False)
