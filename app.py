from flask import Flask, render_template, request, redirect, url_for, session
from database import create_users_table

create_users_table()

app = Flask(__name__)

# Required for session management
app.secret_key = "supersecretkey"


@app.route("/", methods=["GET", "POST"])
def login():
    # If user is already logged in, go directly to dashboard
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Temporary hardcoded check (DB comes later)
        if username == "admin" and password == "1234":
            session["user"] = username   # create session
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"

    # GET request → show login page
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # Protect dashboard
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user from session
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

