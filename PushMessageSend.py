 
import urllib.request
import json 
import datetime
from urllib.error import URLError, HTTPError
import time
import sys
 
##### 準備 #####
# 1) Push のできるアプリはあらかじめ用意しておいてください
# 2) メッセージの作成と送信を繰り返しますので、何度も実施するとメッセージの作成数が大きくなります。 
#    2回目以降は、createdMSG = createPushMessage(res["access_token"]) をコメントアウトして、
#   作成したトリガーメッセージをコンソールに出力しますので、以下の＜ここ＞のところにメッセージIDを入れてください
#   sendMessage(res["access_token"], ＜ここ＞)
 
##### 定数 #####
# パッケージ
clientID = '<Your ClientID>' # 秘密の情報。
clientSecret = ‘<Your ClientSecret>’# 秘密の情報
mid = '<Your MID>'
authURL = "https://<Your TSE>.auth.marketingcloudapis.com/v2/token"
restURL = "https://<Your TSE>.rest.marketingcloudapis.com/" # ちゃんと末尾にスラッシュを入れる！！

# Push 設定
appId = "<Provisioned APP id>"
appName = "<Provisioned APP Name>"
# 送信先の購読者キー
targetContactKey = "<Target Contact Key>"
# メッセージID
messageId = "<Message ID>"
 
#### Methods ####
# 1) 認証トークンの取得@v1
def getAuthentication():
    # HTTP リクエスト定義
    url = authURL
    headers = {
        "Content-Type": "application/json;charset=sjis"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": clientID ,
        "client_secret": clientSecret,
        "account_id": mid
    }  
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   resInJson
      
# 3) メッセージ送信
def sendMessage(token, messageId):  
    url = restURL +  "/push/v1/messageBatch/" + messageId +"/send"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = [
        {
        "SubscriberKeys": [
            targetContactKey
            ]
        }
        
    ]
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   
 
 
### 実処理　####
# トークン取得
res = getAuthentication()
# メッセージ送信
sendMessage(res["access_token"], messageId)
 
