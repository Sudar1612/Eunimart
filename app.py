from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from flask_mongoengine import MongoEngine
from flask import Flask, render_template, request,url_for,session,redirect
import sqlite3 as sql
import json



app = Flask(__name__)


#home page creation
@app.route('/')
def home():
   return render_template('home.html')


#registration
@app.route('/register')
def register():
   return render_template('register.html')

#add created records to db
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']
         gender=request.form['gender']
         age = request.form['age']
         phone = request.form['phone']
         email = request.form['email']
         password = request.form['password']
         
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (UName,ID,Gender,Age,Phone,Email,Password) \
               VALUES (?,?,?,?,?,?,?)",(nm,id,gender,age,phone,email,password) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

#login after succesful registration
@app.route("/login",methods=['GET','POST'])
def login():
   
   if(request.method=="POST"):
      id=request.form['id']
      password=request.form['password']
      conn=sql.connect("database.db")
      c=conn.cursor()
      row=c.execute("SELECT ID,Password FROM users WHERE ID= (?)and Password= (?)",(id,password))
      row=c.fetchall()
      if(len(row)==1):
         msg="Login Successful"
         return render_template("log_result.html",msg=msg)
      else:
         return render_template("register.html")
   return render_template('login.html')


#tweet creation

@app.route('/create_tweet',methods=['GET','POST'])

def create_tweet():
   if request.method == 'POST':
      try:
         id = request.form['id']
         tweet=request.form['tweet']
         date=request.form['date']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO tweet (ID,Tweet,Date) \
               VALUES (?,?,?)",(id,tweet,date) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return  render_template('log_result.html',msg=msg)
         con.close()
   return render_template('create_tweet.html')


#viewing tweets
@app.route('/view_tweet')
def view_tweet():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from tweet")
   
   rows = cur.fetchall();
   return render_template("view_tweet.html",rows = rows)


#tweet deletion
@app.route('/delete_tweet',methods=['GET','POST'])

def delete_tweet():
   if request.method == 'POST':
      try:
         id = request.form['id']
         tweet=request.form['tweet']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM  tweet WHERE ID=(?) AND Tweet=(?)",  (id,tweet))
            
            con.commit()
            msg = "Record successfully deleted"
      except:
         con.rollback()
         msg = "error in deletion operation"
      
      finally:
         return  render_template('log_result.html',msg=msg)
         con.close()
   return render_template('delete_tweet.html')


#users db 
@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from users")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


#main function
if __name__ == '__main__':
   app.run(debug = True)