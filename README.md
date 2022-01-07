# LineStockQuoter
* 這是一個用 Django, Line API 架設並部署在 Heroku 的Line聊天機器人，只要輸入上市股票代號即可回應當日漲跌、成交量等訊息。

<img src="/Screenshot_LINE.jpg" width=20% height=20%>

## 使用技術與工具
* 網頁爬蟲:
    - Python
    - Pandas
    - shioaji
    - dotenv
    - urllib
* 後端:
    - [Django(3.2.7)](https://www.djangoproject.com/)
        - django-allauth(Google、GitHub)  
        - django-shopping-cart
        - djagno-filer
    - [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
* 資料庫:
    - [MySQL](https://www.mysql.com/)
    - [PostgreSQL(Heroku)](https://www.postgresql.org/)
    - [SQLite](https://www.sqlite.org/index.html)
* 部署:
    - [Ngrok](https://ngrok.com/)
    - [Heroku](https://dashboard.heroku.com/)

## 專案上遇到的問題
### Config組態設定
* 因為公開於 github 並部署於 heroku ，當中敏感資訊如: LINE token、帳號、密碼等，容易會有外露的資安問題，所以將散佈檔案中的敏感參數集中在 .env 的組態設定檔，其載入環境變數中作使用，掌控 .env 上傳即可避免敏感資訊曝露，也方便統一管理所需要的參數

### Django套件
* `django-shopping-cart` 內建的 `add` 函式無法存取 product，導致 `OrderItem` 這個 model 無法跟 `Product` 這個 model 以 foreign key 做關聯，地端程式碼可以手動修改，但部署到 Heroku 就無法修改套件py檔內容，因此最後 Heroku app 取消關聯到 `Product` 這個資料表
* `python manage.py makemigrations` 若失效，要進到 `migrations` 資料夾，手動查找每個版本的py檔，找出與model修正有關聯的檔案，手動修正或刪除，重新執行此指令即可成功運行

### line-bot套件
* Django應用程式中需要使用line-bot套件設定 webhook，藉由Messaging API使應用程式與LINE Platform溝通。
* LINE Bot 開發使用到的 webhook 是讓一個網站能訂閱另一個網站的方法，使LINE Platform 及 Bot server 兩端都能同時擔任「發送方」及「接收方」時，能避免掉「發送方」需要「輪詢(Polling)」所造成的資源浪費，LINE Platform 傳遞用戶訊息給 Bot server ，同時 Bot server 也能主動的向用戶藉由 LINE Platform 來進行推播的動作。

### Heroku部署
* Heroku 部署需要提供三個檔案，`Procfile`、`requirements.txt`、`runtime.txt`
* `Procfile`是要告訴 Heroku 要使用 Gunicorn 來啟動 web server
* `requirements.txt`用來告訴Heroku雲端平台有哪些套件需要進行安裝，於專案虛擬環境執行 `pip freeze > requirements.txt` 指令會生成
* `runtime.txt`是用來告訴 heroku 執行程式碼的 Python 版本，若沒指定 heroku 預設安裝最新版 Python，並依`requirements.txt`安裝支援該版本 Python 的套件，但 shioaji 套件目前只有支援到 Python 3.7，必須在`runtime.txt`指定 Python 3.7版，避免於推送程式碼時出現許多找無可用套件而部署失敗
* Heroku 資料庫是使用 PostgreSQL，要手動在 requirements.txt 加上 psycopg2==2.9（Python 的 PostgreSQL 模組)，以及 `settings.py` 裏頭要修改DB連結的方式，才能在 Heroku 上部署成功

