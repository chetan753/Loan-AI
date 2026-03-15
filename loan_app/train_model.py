import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split,cross_val_score





np.random.seed(42)
n = 500

credit_score = np.random.randint(300, 850, n)
income       = np.random.randint(20000, 150000, n)
loan_amount  = np.random.randint(5000, 100000, n)
emp_years    = np.random.randint(0, 30, n)
age          = np.random.randint(21, 65, n)

# realistic approval logic
approved = (
    (credit_score > 650) &
    (income > loan_amount * 0.3) &
    (emp_years > 1)
).astype(int)

x =np.column_stack([credit_score,income,loan_amount,emp_years,age])
y =approved

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
model = LogisticRegression(max_iter=1000)
model.fit(x_train,y_train)

joblib.dump(model,"loan_model_V2.pkl")
print("model saved")