from flask import Flask, redirect, render_template, request, session, url_for
import datetime
import pymongo
from decouple import config
from twilio.rest import Client
##import pyautogui as pag

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################

# MONGODB
#############################################################
mongodb_key = config('mongodb_key')
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Coronavirus
cuentas = db.Usuario
#############################################################


# Twilio
#############################################################
account_sid = config('account_sid')
auth_token = config('auth_token')
TwilioClient = Client(account_sid, auth_token)
#############################################################



@app.route("/insert", methods=["POST"])
def insertUsers():
    user = {
        "matricula": request.form["matricula"],
        "nombre": request.form["nombre"],
        "email": request.form["email"],
        "contrasena": request.form["contrasena"],
    }

    if cuentas.find_one({"email": user['email'] }):
        return render_template("login.html", error= "Este correo ya ha sido utilizado")
      
    else:

        try:
            cuentas.insert_one(user)
            twl = TwilioClient.messages.create(
            from_="whatsapp:+19706708543",
            body="El usuario %s se agregó a tu pagina web" % (
            request.form["nombre"]),
            to="whatsapp:+5215537070576")
            print(twl.sid)
            email=user["email"]
            session["email"]= email

            return render_template('index.html', data=user)

        except Exception as e:
            return "<p>El servicio no esta disponible =>: %s %s" % type(e), e



@app.route('/', methods =["GET"])
def home():
    email = None
    if "email" in session:
        email = session["email"]
        user = cuentas.find_one({"email": (email)})
        
        return render_template('index.html', data=user)
    else:
        return render_template('login.html')
    

@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if "email" in session:
        email=session['email']
        user = cuentas.find_one({"email": (email)})
       
        return render_template('index.html', data=user)
    else:
        if (request.method == "GET"):
            return render_template("login.html", data="email")
        else:
            email=None
            email = request.form["email"]
            password = request.form["contrasena"]

            ExpectedUser = verify(email,password)

            if (ExpectedUser != None):
                session ["email"]=email
                return render_template("index.html", data= ExpectedUser)
            else:
                return render_template("login.html", error= "Usuario o contraseña incorrecta")
                


def verify(email,password):

        Expecteduser = cuentas.find_one({"email": (email), "contrasena": (password)})
        return Expecteduser
'''
            try:
                user = cuentas.find_one({"email": (email)})
                if(user!=None):
                   #Lo encuentra
                    if (user["contrasena"] == password):
                        email = session["correo"]
                        return render_template("Index.html", data=user)
                    else:
                        return render_template("Login.html", error= "Contraseña incorrecta Ahhhh")
                #No lo encuentra     
                else:

                    return render_template("Login.html", error= "Correo incorrecto Ahhhh")
                   
                    
            except Exception as e:
                return "Este es el error %s" % e

'''

#Testasfcn sdkjf c#
                
        
@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))


@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')


@app.route('/create')
def create_form():  
    return render_template('CreateForm.html')


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/Usuarios.html", data=users)

    
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

@app.route("/delete_one/<matricula>")
def delete_one(matricula):
    try:
        
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None and "email" in session:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            session.clear()
            user.deleted_count
            return redirect(url_for("home"))
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