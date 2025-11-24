from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "test"

# 임시 사용자 데이터
USERS = {
    "admin": {"password": "1234", "balance": 500000}
}

#@app.route('/', methods=['GET', 'POST'])
# = 루트 URL에서 GET과 POST 요청을 처리하는 기능을 만들겠다
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = USERS.get(username)
        if user and user["password"] == password:
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            return "로그인 실패!"

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if(username not in session) : 
        return redirect(url_for('login'))
    username = session['username']
    balance = USERS[username]["balance"]
    return render_template("dashboard.html", username=username, balance=balance)