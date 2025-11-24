from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "test"

# 임시 사용자 데이터
USERS = {
    "admin": {"password": "1234", "balance": 500000}
}
# 라우팅 : 웹에서 url과 처리 함수를 연결
# 서버는 어떤 코드를 실행해야하는 지 알아야 한다.

#flask의 기본구조
#1. @app.route()    → URL 등록
#2. 함수            → 실행할 코드
#3. return          → HTML or redirect
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #사용자가 입력 후 제출하면 서버가 POST 데이터를 받고
        #request.form 딕셔너리에 담깁니다.
        username = request.form['username']
        password = request.form['password']

        #이제 서버가 사용자 정보를 저장한 데이터베이스(혹은 딕셔너리)에서
        #실제 계정 정보를 가져오는 것
        user = USERS.get(username)
        #세션은 브라우저와 서버가 
        #로그인 상태를 기억하도록 하는 방법입니다.
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
        account_number = request.form['account_number']  # 수정됨

        USERS[username]["balance"] -= amount

        # 계좌번호와 금액을 세션에 저장
        session['last_account'] = account_number
        session['last_amount'] = amount

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)