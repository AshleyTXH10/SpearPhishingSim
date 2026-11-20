from datetime import datetime
from flask import Flask, request, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
  print(
      f"[{datetime.now()}] Page opened | IP:"
      f" {request.headers.get('X-Forwarded-For', request.remote_addr)}"
  )
  return send_from_directory(".", "training.html")


@app.route("/<path:filename>")
def static_files(filename):
  return send_from_directory(".", filename)


@app.route("/submit", methods=["POST"])
def submit():
  # Log only non-sensitive simulation telemetry (avoid storing raw passwords)
  submitted_fields = list(request.form.keys())
  print(
      f"[{datetime.now()}] Form submitted | Fields: {submitted_fields} |"
      f" IP: {request.headers.get('X-Forwarded-For', request.remote_addr)}"
  )
  return "Simulation recorded.", 200


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5001)
