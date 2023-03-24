from citasBd import Connection


def insertar_paciente(Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion):
    conexion = Connection()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Pacientes(Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)",
                       (Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion))
    conexion.commit()
    conexion.close()


def obtener_Pacientes():
    conexion = Connection()
    citas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT Id, Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion FROM Pacientes")
        citas = cursor.fetchall()
    conexion.close()
    return citas


def eliminar_paciente(Id):
    conexion = Connection()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Pacientes WHERE Id = %s", (Id,))
    conexion.commit()
    conexion.close()


def obtener_paciente_por_id(id):
    conexion = Connection()
    Paciente = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT Id, Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion FROM Pacientes WHERE Id = %s", (id,))
        Paciente = cursor.fetchone()
    conexion.close()
    return Paciente


def actualizar_paciente(Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion, Id):
    conexion = Connection()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Pacientes SET Nombre = %s, Primer_Apellido = %s, Segundo_Apellido = %s, Edad = %s, Tipo_de_Sangre = %s, Numero_Telefonico = %s, Correo = %s, Direccion = %s WHERE Id = %s",
                       (Nombre, Primer_Apellido, Segundo_Apellido, Edad, Tipo_de_Sangre, Numero_Telefonico, Correo, Direccion, Id))
    conexion.commit()
    conexion.close()

  