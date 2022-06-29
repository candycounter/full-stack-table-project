import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
import pandas as pd

pdata4 = pd.read_csv('./employee_data.csv', index_col=False, delimiter=',')

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               passwd='awesomedude',
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

            # in the below line please pass the create table statement which you want #to create
            st = "CREATE TABLE employee_data(first_name varchar(255), last_name varchar(255), education varchar(255), \
            year_hired int, id int, role varchar(255))"
            cursor.execute(st)
            print('reached')
            print("Table is created....")
            # loop through the data frame
            for i, row in pdata4.iterrows():
                # here %S means string values
                sql = "INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                mydb.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)


@app.route('/getemployees')
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
    employee_id = data['employee_id']
    role = data['role']
    val = (first_name, last_name, education, year_hired, employee_id, role)
    stmnt = "INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s)"
    print(stmnt)
    cursor.execute(stmnt, val)
    mydb.commit()

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
    print("Done")
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





