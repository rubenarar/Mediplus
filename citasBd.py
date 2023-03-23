import mysql.connector
def Connection():
    return mysql.connector.connect(host='localhost',
                                user='root',
                                password='root',
                                db='citas')

