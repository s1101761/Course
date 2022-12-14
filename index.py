
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from datetime import datetime, timezone, timedelta
from flask import Flask, render_template,request,make_response, jsonify
app = Flask(__name__)



@app.route("/")
def index():
    homepage = "<h1>顏偉森Firestore資料庫存取</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=顏偉森>傳送使用者暱稱</a><br>"
    homepage += "<a href=/I>顏偉森簡介網頁</a><br>"
    homepage += "<a href=/text>職涯測驗結果</a><br>"
    homepage += "<a href=/jobsearch>個人求職自傳履歷網頁</a><br>"
    homepage += "<a href=/Interestwork>感興趣的工作網頁</a><br>"
    homepage += "<a href=/account>表單</a><br>"
    homepage += "<a href=/search>課程查詢</a><br><br>"
    homepage += "<a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br><br>"
    homepage += "<a href=/query>電影查詢</a><br><br>"
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

@app.route("/text")
def text():
    return render_template("text.html")


@app.route("/jobsearch")
def jobsearch():
    return render_template("jobsearch.html")
    
@app.route("/Interestwork")
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
        
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cond = request.form["Course"]
        cond2 = request.form["Leacture"]
        result = "您輸入的課程關鍵字是：" + cond 

        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()

        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"] and cond2 in dict["Leacture"]:
                result += dict["Leacture"] + "老師開的" + dict["Course"] + "課程,每週"
                result += dict["Time"] + "於" + dict["Room"] + "上課<br>"
        
        if result =="":
            result += "抱歉，查無相關條件的選修課程"
        return result
        
    else:
        return render_template("search.html")
        
        
@app.route("/movie")
def movie():
    return render_template("movie.html")        
        
@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        cond = request.form["query"]
        result = "您輸入的片名關鍵字是：" + cond 

        db = firestore.client()
        collection_ref = db.collection("偉森的電影")
        docs = collection_ref.get()

        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["title"]:
                result += "片名:<a href=" + dict["hyperlink"] + ">" + dict["title"] + "</a><br>電影分級:" + dict["rate"] + "<br><br>"
        
        if result =="":
            result += "抱歉，查無相關條件的電影資訊"
        return result
        
    else:
        return render_template("query.html")
        
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req.get("queryResult").get("action")
    if (action == "dramaC"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的戲劇分類是：" + rate + "，相關戲劇：\n"
        collection_ref = db.collection("最新劇集_全部")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    if (action == "dramaC"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的戲劇分類是：" + rate + "，相關戲劇：\n"
        collection_ref = db.collection("最新劇集_分類")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    if (action == "movieC"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的電影分類是：" + rate + "，相關電影：\n"
        collection_ref = db.collection("最新電影_全部")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    if (action == "movieC"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的電影分類是：" + rate + "，相關電影：\n"
        collection_ref = db.collection("最新電影_分類")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    if (action == "cartoonC"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的動漫分類是：" + rate + "，相關動漫：\n"
        collection_ref = db.collection("最新動漫_全部")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
        info += result

    elif (action == "CityWeather"):
        city =  req.get("queryResult").get("parameters").get("city")
        token = "rdec-key-123-45678-011121314"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + token + "&format=JSON&locationName=" + str(city)
        Data = requests.get(url)
        Weather = json.loads(Data.text)["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
        Rain = json.loads(Data.text)["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
        MinT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
        MaxT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
        info = city + "的天氣是" + Weather + "，降雨機率：" + Rain + "%"
        info += "，溫度：" + MinT + "-" + MaxT + "度"

    return make_response(jsonify({"fulfillmentText": info}))
        

if __name__ == "__main__":
    app.run()
    
