import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
import requests
from bs4 import BeautifulSoup

# 定義包含所有集合名稱的列表
collections = ["最新劇集_全部", "最新劇集_分類", "最新電影_全部", "最新電影_分類", "最新動漫_全部"]

# 使用迴圈將列表中的每個集合都刪除
for collection in collections:
    batch = db.batch()
    # 列出集合中的所有文件
    docs = db.collection(collection).list_documents()
    # 個別將每筆文件添加至批量刪除的批次中
    for doc in docs:
        batch.delete(doc)
    # 執行批量刪除
    batch.commit()

def crawl_and_store_new_episodes(url, collection_name, rate):
  data = requests.get(url)
  data.encoding = "utf-8"
  sp = BeautifulSoup(data.text, "html.parser")

  h4_titles = sp.find_all("h4", class_="title")
  for h4_title in h4_titles[:10]:
    text = h4_title.text # 取出 h4 標題的文字內容
    link = "https://jumi.tv/" + h4_title.find("a").get("href") # 取出 h4 標題的文字超連結

    # 使用劇集名稱作為文件 ID
    movie_id = text

    doc = {
      "text": text, #最新劇集名稱
      "link": link,  #最新劇集網址
      "rate": rate
    }
    doc_ref = db.collection(collection_name).document(movie_id)
    doc_ref.set(doc)

# 爬取最新 10 部劇集
crawl_and_store_new_episodes("https://jumi.tv/show/2/year/2022.html", "最新劇集_全部", "全部")

# 爬取最新 10 部陸劇
crawl_and_store_new_episodes("https://jumi.tv/show/13/year/2022.html", "最新劇集_分類", "陸劇")
# 爬取最新 10 部港劇
crawl_and_store_new_episodes("https://jumi.tv/show/14/year/2022.html", "最新劇集_分類", "港劇")
# 爬取最新 10 部台劇
crawl_and_store_new_episodes("https://jumi.tv/show/22/year/2022.html", "最新劇集_分類", "台劇")
# 爬取最新 10 部日劇
crawl_and_store_new_episodes("https://jumi.tv/show/15/year/2022.html", "最新劇集_分類", "日劇")
# 爬取最新 10 部韓劇
crawl_and_store_new_episodes("https://jumi.tv/show/23/year/2022.html", "最新劇集_分類", "韓劇")
# 爬取最新 10 部美劇
crawl_and_store_new_episodes("https://jumi.tv/show/16/year/2022.html", "最新劇集_分類", "美劇")
# 爬取最新 10 部海外劇
crawl_and_store_new_episodes("https://jumi.tv/show/24/year/2022.html", "最新劇集_分類", "海外劇")

# 爬取最新 10 部電影
crawl_and_store_new_episodes("https://jumi.tv/show/1/year/2022.html", "最新電影_全部", "全部")

# 爬取最新 10 部動作片電影
crawl_and_store_new_episodes("https://jumi.tv/show/6/year/2022.html", "最新電影_分類", "動作片")
# 爬取最新 10 部喜劇片電影
crawl_and_store_new_episodes("https://jumi.tv/show/7/year/2022.html", "最新電影_分類", "喜劇片")
# 爬取最新 10 部愛情片電影
crawl_and_store_new_episodes("https://jumi.tv/show/8/year/2022.html", "最新電影_分類", "愛情片")
# 爬取最新 10 部科幻片電影
crawl_and_store_new_episodes("https://jumi.tv/show/9/year/2022.html", "最新電影_分類", "科幻片")
# 爬取最新 10 部恐怖片電影
crawl_and_store_new_episodes("https://jumi.tv/show/10/year/2022.html", "最新電影_分類", "恐怖片")
# 爬取最新 10 部劇情片電影
crawl_and_store_new_episodes("https://jumi.tv/show/11/year/2022.html", "最新電影_分類", "劇情片")
# 爬取最新 10 部戰爭片電影
crawl_and_store_new_episodes("https://jumi.tv/show/12/year/2022.html", "最新電影_分類", "戰爭片")
# 爬取最新 10 部紀錄片電影
crawl_and_store_new_episodes("https://jumi.tv/show/20/year/2022.html", "最新電影_分類", "紀錄片")

# 爬取最新 10 部動漫
crawl_and_store_new_episodes("https://jumi.tv/show/4/year/2022.html", "最新動漫_全部", "全部")