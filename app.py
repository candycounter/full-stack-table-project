import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request, redirect, url_for
import pandas as pd
import random

pdata = pd.read_csv('./employee_data.csv', index_col=False, delimiter=',')

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               passwd='********',
                               database='db')
cursor = mydb.cursor()

app = Flask(__name__)



@app.route('/create/table')
def create_table():
    try:
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        if mydb.is_connected():
            cursor.execute('DROP TABLE IF EXISTS employee_data;')

            st = "CREATE TABLE employee_data(first_name varchar(255), last_name varchar(255), education varchar(255), \
            year_hired int, id int, role varchar(255))"
            cursor.execute(st)

            for i, row in pdata.iterrows():
                sql = "INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                mydb.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)


@app.route('/getemployees', methods=['GET'])
def employee_data():
    query = "SELECT * FROM employee_data"
    cursor.execute(query)
    records = cursor.fetchall()
    employee_list = []

    for employee in records:
        current_employee = {
            "name": employee[0] + " " + employee[1],
            "role": employee[5],
            "id": employee[4],
            "education": employee[2],
            "year_hired": employee[3]
        }
        employee_list.append(current_employee)
    return jsonify(employee_list)


@app.route('/addemployee', methods=['POST'])
def add_employee():
    data = request.json
    first_name = data['first']
    last_name = data['last']
    education = data['education']
    year_hired = data['year_hired']
    employee_id = random.randint(100000000, 900000000)
    role = data['role']
    val = (first_name, last_name, education, year_hired, employee_id, role)
    stmnt = "INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(stmnt, val)
    mydb.commit()

    return redirect(url_for('employee_data'))


@app.route('/removeemployee', methods=['POST'])
def remove_employee():
    data = request.json
    first_name = data['first']
    last_name = data['last']
    employee_id = data['employee_id']
    query = "DELETE FROM employee_data WHERE first_name = %s AND last_name = %s AND id = %s"
    val = (first_name, last_name, employee_id)
    cursor.execute(query, val)
    mydb.commit()

    return redirect(url_for('employee_data'))


@app.route('/updateemployee', methods=['POST'])
def update_role():
    data = request.json
    role = data['role']
    employee_id = data['employee_id']
    query = "UPDATE employee_data \
            SET role = %s \
            WHERE id = %s"
    val = (role, employee_id)
    cursor.execute(query, val)
    mydb.commit()
    return redirect(url_for('employee_data'))






