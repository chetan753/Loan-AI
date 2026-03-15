from flask import Flask,render_template,request,session,redirect
import random
import joblib
import sqlite3
import pandas as pd




app = Flask(__name__)
app.secret_key = "your_secret_key"

model = joblib.load("loan_model.pkl")

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS calculations (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       num1 REAL,
                       num2 REAL,
                       action TEXT,
                       result REAL)""")
    conn.commit()
    conn.close()
init_db()    



@app.route("/",methods = ["GET",'POST'])
def home():
    
    result = ""
    result1 = ""
    
    
    
    if request.method == "POST":
        num = request.form.get("username")
        num1 = request.form.get("usernum")
        action = request.form.get("action")
        if action == "square":
            try:
                number = int(num)
                result = f"Square of {num} is {number*number}"
            except (ValueError, TypeError):
                result = "please enter a vaild number"    
            
        elif action == "cube":
            try:
                number = int(num1)
                result1 = f"cube of {num1} is {number*number*number}"
            except (ValueError, TypeError):
                result1 = "please enter a vaild number"
            
                
    return render_template("index.html",result=result,result1=result1)


@app.route("/home1",methods=["GET","POST"])

def home1():
    
    result2 = " "
    
    if "number" not in session:
        session["number"] = random.randint(1,100)
    
    if request.method == "POST":
        if "reset" in request.form:
            session.pop("number", None)
            session["number"] = random.randint(1,100)
            result2 = "Reset!"
            return render_template("index1.html",result2 = result2)
        try:
            num =  int(request.form.get("userguess"))
            our_guess = session["number"]
            if num == our_guess:
                result2 = f"Guess number = {our_guess} Conragulation your guess was right!"               
            elif num < our_guess:
                result2 = "Inncorrect!,Hint: number is higher than your guess"
            elif num > our_guess:
                result2 = "Inncorrect!,Hint: number is lower than your guess"
            else:
                result2 = "Please enter a valid number!" 
        except (ValueError, TypeError):
            result2 = "Enter valid number only!!"                
    return render_template("index1.html", result2=result2)


@app.route("/loan",methods= ["GET","POST"])

def loan():
    result3 = ""
    if request.method == "POST":
        try:
            credit = int(request.form.get("cerdit"))
            income = int(request.form.get("income"))
            loanamount = int(request.form.get("loanamount"))
            prediction=model.predict_proba([[income,credit,loanamount]])[0][1]
            threshold = 0.7
            if (prediction>=threshold).astype(int):
                result3 = f" Apporved probability={prediction:.2f}"
            else:
                result3 = f"Denied probablity={prediction:.2f}"
            return render_template("loan.html",result3=result3) 
        except (ValueError,TypeError):
            result3 = "Enter valid number"
            return render_template("loan.html", result3 = result3)  
    
    return render_template("loan.html")


    

@app.route("/calculator",methods=["GET","POST"])

def calculator():
    result4 = ""
    if request.method == "POST":
        result4 = ""
        num1 = request.form.get("num1")
        num2 = request.form.get("num2") 
        action = request.form.get("action")
        if num1 and num2:
            num1 = float(num1)
            num2 = float(num2)
        try:
            if action == "add":
                result4 = num1+num2
            elif action == "sub":
                result4 = num1-num2
            elif action == "multiply":
                result4 = num1*num2
            elif action == "div":
                if num2 == 0:
                    result4 = "cannot divide 0"
                else:
                    result4 = num1/num2
        except (ValueError,TypeError):
            result = "Enter vaild number only!!" 
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calculations (num1,num2,action,result) VALUES (?, ?, ?, ?)",(num1,num2,action,result4)
        )               
        conn.commit()
        conn.close()  
        
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
        
    cursor.execute("SELECT * FROM calculations")
    history = cursor.fetchall()
    conn.close() 
    return render_template("calculator.html",result4=result4, history=history)

@app.route("/delete/<int:id>")

def delete(id):
    print("deleting ID:",id)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculations WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect("/calculator")

@app.route("/clear")

def clear():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculations")
    conn.commit()
    conn.close()
    return redirect("/calculator")
     

if __name__=="__main__":
    app.run(debug=True)
    
    