from flask import Flask,redirect,render_template,request
import joblib
import sqlite3

model=joblib.load("loan_model_V2.pkl")

app = Flask(__name__)

def int_db():
    
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
                   
                   
                   CREATE TABLE IF NOT EXISTS history (
                       
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        credit_score INETGER,
                        income INTEGER,
                        loan_amount INTEGER,
                        emp_years INTEGR,
                        result TEXT,
                        prob INTEGER
                    )""")

    conn.commit()
    conn.close()
int_db()  

@app.route("/",methods=["GET","POST"])
def home():
    result = ""
    return render_template("home.html",result=result)

@app.route("/predict",methods=["GET",'POST'])

def predict():
    result1 = None
    probability=None
    loan_amt=None
    credit_score=None
    income=None
    emp_years=None
    if request.method=="POST":
        credit_score = int(request.form.get("credit_score"))
        income = int(request.form.get("income"))
        loan_amt = int(request.form.get("loan_amount"))
        emp_years = int(request.form.get("emp_years"))
        age = int(request.form.get("age"))
        preds = model.predict_proba([[credit_score,income,loan_amt,emp_years,age]])
        treshold = 0.7
        probability=round(preds[0][1]*100,1)
        if preds[0][1]>treshold:
            result1 = "Approved"
        else:
            result1="Denied"
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    
    cursor.execute(
                   "INSERT INTO history (credit_score,income,loan_amount,emp_years,result,prob) VALUES (?,?,?,?,?,?)",(credit_score,income,loan_amt,emp_years,result1,probability))
    conn.commit()
    conn.close()
    
    
    
    
        
    return render_template("predict.html",result1=result1,probability=probability,credit_score=credit_score,income=income,emp_years=emp_years)

@app.route("/history",methods=["GET","POST"])
def history():
    result2 =None
    history=None
    conn = sqlite3.connect("history.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    history = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("history.html",result2=result2,history=history)

@app.route("/delete/<int:id>",methods=["POST","GET"])

def delete(id):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/history")

@app.route("/stats",methods=["GET"])
def stats():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM history")
    total = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM history WHERE result=?", ("Approved",))
    approved = cursor.fetchone()[0] or 0
    rejected = total - approved
    approval_rate = round((approved / total * 100), 1) if total else 0
    cursor.execute("SELECT COUNT(*) FROM history WHERE prob >= 70")
    low_risk = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM history WHERE prob >= 40 AND prob < 70")
    med_risk = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM history WHERE prob < 40")
    high_risk = cursor.fetchone()[0] or 0
    low_pct = round((low_risk / total * 100), 1) if total else 0
    med_pct = round((med_risk / total * 100), 1) if total else 0
    high_pct = round((high_risk / total * 100), 1) if total else 0
    cursor.execute("SELECT AVG(credit_score), AVG(income), AVG(loan_amount) FROM history")
    row = cursor.fetchone()
    avg_credit = round(row[0], 1) if row and row[0] is not None else 0
    avg_income = round(row[1], 0) if row and row[1] is not None else 0
    avg_loan = round(row[2], 0) if row and row[2] is not None else 0
    conn.close()
    return render_template("stats.html", total=total, approved=approved, rejected=rejected,
                          approval_rate=approval_rate, low_risk=low_risk, med_risk=med_risk, high_risk=high_risk,
                          low_pct=low_pct, med_pct=med_pct, high_pct=high_pct,
                          avg_credit=avg_credit, avg_income=avg_income, avg_loan=avg_loan)

@app.route("/clear",methods=["GET","POST"])
def clear():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return redirect("/history")
if __name__ =="__main__":
    app.run(debug=True)