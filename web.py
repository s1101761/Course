from flask import Flask, render_template,request
from datetime import datetime
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>顏偉森Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=顏偉森>傳送使用者暱稱</a><br>"
    homepage += "<a href=/I>顏偉森簡介網頁</a><br>"
    homepage += "<a href=/A>職涯測驗結果</a><br>"
    homepage += "<a href=/B>個人求職自傳履歷網頁</a><br>"
    homepage += "<a href=/C>感興趣的工作網頁</a><br>"
    homepage += "<a href=/account>表單</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/I")
def about():
    return render_template("about.html")

@app.route("/A")
def text():
    return render_template("text.html")


@app.route("/B")
def jobsearch():
    return render_template("jobsearch.html")
    
@app.route("/C")
def Interestwork():
    return render_template("Interestwork.html")
    
@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

#if __name__ == "__main__":
 #   app.run()
    
