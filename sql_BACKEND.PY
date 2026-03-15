import sqlite3
from numpy import column_stack
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error

conn = sqlite3.connect("database.db")
df =pd.read_sql_query("SELECT hours_studied,score,age,city FROM students",conn)
conn.close()
df = pd.get_dummies(df, columns= ["city"])
x = df.drop("score", axis=1)
y = df["score"]

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
model = LinearRegression()
model.fit(x_train,y_train)

preds = model.predict(x_test)
print("MEA:",mean_absolute_error(y_test,preds))
print("R^2",r2_score(y_test,preds))
