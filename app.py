from flask import Flask, render_template,redirect,request,session
from flask_mail import Mail, Message
import mysql.connector
import citasRedirect
Connection = mysql.connector.connect(host='localhost',
                                user='root',
                                password='root',
                                db='Mediplus')

cursor = Connection.cursor()
app = Flask(__name__)
app.secret_key="super secret key"

@app.route('/')
def index_():
    return redirect('/login.html')

@app.route ('/login.html')
def login():
    return render_template ('login.html')

@app.route ('/registro.html')
def register():
    return render_template ('registro.html')

@app.route ('/index.html')
def index():
    if session['logeado']==True:  
        return render_template('index.html', username=session['username'])    
    else:    
        return redirect('/login')

@app.route ('/contacto.html')
def contacto():
    return render_template('contacto.html')

@app.route ('/acercade.html')
def acercade():
    return render_template ('acercade.html')

@app.route ('/citas.html')
def citas():
    citas = citasRedirect.obtener_Pacientes()
    return render_template ('citas.html', citas=citas, username=session['username'])

@app.route("/formulario_editar_cita/<int:id>")
def editar_cita(id):
    cita = citasRedirect.obtener_paciente_por_id(id)
    return render_template("editar_cita.html", cita=cita)

@app.route("/actualizar_paciente", methods=["POST"])
def actualizar_paciente():
    Id = request.form ["id"]
    Nombre = request.form["nombre"]
    Primer_Apellido = request.form["primer_apellido"]
    Segundo_Apellido = request.form["segundo_apellido"]
    Edad = request.form["edad"]
    Tipo_de_Sangre = request.form["tipo_sangre"]
    Numero_telefonico = request.form["numero_telefonico"]
    Correo = request.form["correo"]
    Direccion = request.form["direccion"]
    citasRedirect.actualizar_paciente(Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_telefonico, Correo, Direccion, Id)
    return redirect ("/citas.html")

@app.route("/eliminar_paciente", methods=["POST"])
def eliminar_paciente():
    citasRedirect.eliminar_paciente(request.form["id"])
    return redirect("/citas.html")

@app.route('/guardar_paciente', methods=['POST'])
def guardar_paciente():
    Nombre = request.form["nombre"]
    Primer_Apellido = request.form["primer_apellido"]
    Segundo_Apellido = request.form["segundo_apellido"]
    Edad = request.form["edad"]
    Tipo_de_Sangre = request.form["tipo_sangre"]
    Numero_telefonico = request.form["numero_telefonico"]
    Correo = request.form["correo"]
    Direccion = request.form["direccion"]
    citasRedirect.insertar_paciente(Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_telefonico, Correo, Direccion)
    return redirect("/citas.html") 


@app.route('/register', methods=['POST'])
def registeruser():
    username = request.form['username']
    password = request.form['password']
    Query = f"INSERT INTO usuarios (username, password) VALUES (%s, %s)"
    cursor.execute(Query,(username, password))
    Connection.commit()
    return redirect("/login")

@app.route('/login', methods=['GET','POST'])
def loginuser():
    msg=''
    if request.method=='POST':
        username =request.form['username']
        password = request.form["password"]
        cursor.execute("SELECT username, password FROM usuarios WHERE username=%s AND password=%s",(username, password))
        record = cursor.fetchone()
        if record: 
                session['logeado']=True 
                session['username']= record[0]  
                return redirect("/index.html") 
    return render_template('login.html', msg=msg)

@app.route ('/agendar.html')
def agendar():
    return render_template ('agendar.html')

# configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rubenoctaviorodriguezcano@gmail.com'
app.config['MAIL_PASSWORD'] = 'qzgbacjowbngufse'
app.config['MAIL_DEFAULT_SENDER'] = 'rubenoctaviorodriguezcano@gmail.com'

mail = Mail(app)

@app.route('/agendar_citas', methods=['POST'])
def agendar_citas():
    nombre = request.form['nombre']
    numero = request.form['numero']
    correo = request.form['correo']
    sintomas = request.form['sintomas']
    fecha = request.form['fecha']
    departamento = request.form['departamento']
    genero = request.form['genero']
    hora = request.form['hora']
    #mensaje
    body = f"""\
    TIENES UNA NUEVA CITA
    Datos de la cita:
    Nombre: {nombre}
    Numero: {numero}
    Correo: {correo}
    Sintomas: {sintomas}
    Fecha: {fecha}
    Hora: {hora}
    Departamento: {departamento}
    Genero: {genero}
    """
    #SEND msg
    msg = Message('Nueva Cita', recipients=[correo])
    msg.body = body
    mail.send(msg)
    return render_template('agendar.html', mensaje='La cita se ha creado exitosamente')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    