
from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for
import datetime


# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################


@app.route('/')
def home():
    email = None
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data=email)
    else:
        return render_template('login.html', data=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if "email" in session:
        return render_template('index.html', data=session["email"])
    else:
        if (request.method == "GET"):
            return render_template("login.html", data="email")
        else:
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email
            return render_template("index.html", data=email)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if (request.method == "GET"):
        return render_template("login.html", data="name")
    else:
        email = None
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        return render_template("index.html", data=name)


@app.route("logout")
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))


@app.route('/estructuradedatos')
def prueba():
    nombres = []
    nombres.append({"nombre": "ruben",

                    "Semetre01": [{
                        "matematicas": "8",
                        "español": "7"
                    }],
                    "Semetre02": [{
                        "programacion": "5",
                        "basededatos": "9"
                    }]
                    })

    return render_template("home.html", data=nombres)
