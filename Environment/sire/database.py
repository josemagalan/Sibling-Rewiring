from flask import Flask, json, request
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="Password", database="prueba")


mycursor = mydb.cursor()

def create_table():
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_user(user_id INT AUTO_INCREMENT PRIMARY KEY,user_name VARCHAR(45) NULL, user_surname VARCHAR(45) NULL,user_username VARCHAR(45) NULL,user_password VARCHAR (45) NULL)")

def create_procedure():
	mycursor.execute("DROP PROCEDURE IF EXISTS sp_createUser")
	file = open('procedure.txt','r')
	query = file.read()
	mycursor.execute(query)

def insert_user(name, surname, passwd):
    sql = ("INSERT INTO users(name, surname, password) VALUES(%s,%s, %s)")
    name = name
    surname = surname
    passwd = passwd
    val = (name, surname, passwd)
    mycursor.execute(sql, val)
    mydb.commit()
    return 'OK'

def signUp():
	try:
		_name = request.form['name']
		_surname = request.form['surname']
		_username =  request.form['username']
		_password = request.form['password']
		
		
		if _name and _surname and _username and _password:
			mycursor.callproc('sp_createUser2',(_name,_username,_surname,_password))
			data = mycursor.fetchall()
			
			if len(data) == 0:
				mydb.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()
		mycursor.close() 
		mydb.close()
		
		
		
create_table()
create_procedure()