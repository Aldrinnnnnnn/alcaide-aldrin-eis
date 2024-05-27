import mysql.connector

class Connector:
    db = mysql.connector.connect(host="localhost", user="root", password="", database="employee_information_system")
    cursor = db.cursor()
