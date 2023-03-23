from flask import Flask, render_template,redirect,request,session
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

@app.route("/editar_cita", methods=["POST"])
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

@app.route('/guardar_citas', methods=['POST'])
def guardar_citas():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    