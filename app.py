from flask import Flask, render_template, render_template_string, redirect, url_for
from flask import request, jsonify

app = Flask(__name__)

# Synthetic demonstration data
stats = {
    "test_visits": 0,
    "password-clicks": 0,
    "signup-clicks": 0,
}

@app.route("/")
def home():
    stats["test_visits"] += 1
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <meta http-equiv="refresh" content="3">
    <h1>Spear Phishing Dashboard</h1>

    <h2>Web visits: {{ visits }}</h2>
    <h2>Login clicks: {{ activity_a }}</h2>
    <h2>Signup clicks: {{ activity_b }}</h2>
    """,
    visits=stats["test_visits"],
    activity_a=stats["password-clicks"],
    activity_b=stats["signup-clicks"])


@app.route("/test-visit", methods=["POST"])
def test_visit():
    stats["test_visits"] += 1
    return redirect(url_for("dashboard"))


@app.route("/record-interaction", methods=["POST"])
def record_interaction():
    data = request.get_json(silent=True) or {}
    interaction = data.get("type")

    if interaction == "password_click":
        stats["password-clicks"] += 1
    elif interaction == "signup_click":
        stats["signup-clicks"] += 1
    else:
        return jsonify({"error": "Invalid interaction"}), 400

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)