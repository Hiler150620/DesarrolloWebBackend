
import email
from flask import Flask, redirect, render_template, request, session, url_for
import datetime
import pymongo
from twilio.rest import Client

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################

# MONGODB
#############################################################
mongodb_key = "mongodb+srv://CarlosGarcia:<password>@cluster0.2hy4l.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Coronavirus
cuentas = db.Usuario
#############################################################

#TWILIO
#############################################################
account_sid = config('AC3104cda267efdd7820039597bdca3add')
auth_token = config('7cdd710e5c8d66b3db6006e15b6c7e0c')
TwilioClient = Client(account_sid, auth_token)
#############################################################


@app.route('/')
def home():
    email = None
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data=email)
    else:
        return render_template('login.html', data=email)


@app.route('/login', methods=["GET", "POST"])
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


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if (request.method == "GET"):
        return render_template("login.html", data="name")
    else:
        email = None
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        return render_template("index.html", data=name)


@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/Usuarios.html", data=users)


@app.route("/insert")
def insertUsers():
    user = {
        "matricula": request.form["matricula"],
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "contrasena": request.form["contrasena"],
    }

    try:
        cuentas.insert_one(user)
        whatsapp = TwilioClient.messages.create(
            from_="whatsapp:+19706708543",
            body="El usuario %s se agregó a tu pagina web" % (
                request.form["nombre"]),
            to="whatsapp:+5215537070576"
        )
        print(whatsapp.sid)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no esta disponible =>: %s %s" % type(e), 


@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula": (matricula)})
        if user == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e

@app.route("/delete/<matricula>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Eliminamos %d matricula: %s </p>" % (user.deleted_count, matricula)
    except Exception as e:
        return "%s" % e

@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        user = {"$set": {
            "nombre": request.form["nombre"]
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return "error %s" % (e)

@app.route('/create')
def create():
    return render_template('Create.html')
