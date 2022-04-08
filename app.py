from crypt import methods
from flask import Flask, render_template, request

# FlASK
#############################################################
app = Flask(__name__)
#############################################################

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/loginuser",methods=["POST"])
def loginuser():
    email = request.form["email"]
    password = request.form["password"]
    return render_template("login.html")

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
