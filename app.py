from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

app.secret_key = "test"

# 임시 사용자 데이터
USERS = {
    "admin": {"password": "1234", "balance": 500000}
}

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
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    balance = USERS[username]["balance"]

    return render_template("dashboard.html", username=username, balance=balance)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        amount = int(request.form['amount'])
        account_number =request.form[account_number] #계좌 번호 내역 추가
        USERS[username]["balance"] -= amount
        return redirect(url_for("accountsend"))

    return render_template("transfer.html", username=username)

@app.route('/accountsend')
def accountsend():
    if 'username' not in session:
        return redirect(url_for('login'))

    account_number = session.get('last_account')
    amount = session.get('last_amount')

    return render_template("accountsend.html", account_number=account_number, amount=amount)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
