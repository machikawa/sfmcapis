 
import urllib.request
import json 
import datetime
from urllib.error import URLError, HTTPError
import time
import sys
 
##### 準備 #####
# 1) Push のできるアプリはあらかじめ用意しておいてください
 
##### 注意 #####
# メッセージを作成したら MessageID をコンソールに出力しますので、
# MessageIDをメモして、メッセージ送信のAPIを実行してください。
 
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
# メッセージ名
messageName = "Pythonからメッセージ送る"
# メッセージ内容
alertMessageBody = "😭"
 
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
      
# 2) Message作成
def createPushMessage(token):
    url = restURL + "/push/v1/message"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {
      "messageType": 1,
      "contentType": 1,
      "name": messageName,
      "application": {
          "id": appId,
          "name":  appName
      },
      "alert": alertMessageBody,
      "Title": "タイトルです",
      "status": 2 ,
      "sendInitiator": 1,
      "startDate": "2022-02-17T00:50:00Z"
    }  
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   resInJson["id"]
 
### 実処理　####
# トークン取得
res = getAuthentication()
# メッセージ作成
createdMSG = createPushMessage(res["access_token"])
print("メッセージ作成が完了しました。MessageID: " + createdMSG + " を使ってください")
