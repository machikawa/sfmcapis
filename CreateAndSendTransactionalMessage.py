#############
# Transactional Message の API を実行
#############
import urllib.request
import json 
import datetime
from urllib.error import URLError, HTTPError
import time
import sys
import random, string
##### 準備 #####
# 1) コンテンツビルダーで送信に使うメールのカスタマーキーを控えておく
# 2) Email Studio - 購読者 - すべての購読者 - プロパティとクリックし
# すべての購読者の外部キーを控えておく (All Subscribers - 2669xx　など)
 
##### 定数 #####
# パッケージ
clientID = '<Your ClientID>' # 秘密の情報。
clientSecret = ‘<Your ClientSecret>’# 秘密の情報
mid = '<Your MID>'
authURL = "https://<Your TSE>.auth.marketingcloudapis.com/v2/token"
restURL = "https://<Your TSE>.rest.marketingcloudapis.com/" # ちゃんと末尾にスラッシュを入れる！！
 
##### メッセージ作成関係 #####
# メッセージのキー。送信時のURLにつかう。 !!重複禁止!! m面倒な時はコメントアウト部分を解除してください
defkey = "DefName" + "".join(random.choices(string.ascii_letters + string.digits, k=8))
# メッセージの名前  !!重複禁止!!面倒な時はコメントアウト部分を解除してください
msgName = "MsgName" + "".join(random.choices(string.ascii_letters + string.digits, k=8))
# 送信に使うコンテンツのカスタマーキー。　Contact Builderで確認できる (準備の 1)) 
emailCustomerKey = "<Email Content Customer Key>"
# すべての購読者の外部キー. Email Studio で確認できる (準備の 2))
listExternalKey = "All Subscribers - <Number>"
# 送信先購読者情報
contactKey = "<target Contact Key>"
email = "<TargetMessage Email>"
 
#####################################
# あなたの情報の入力はここまで
#####################################
 
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
 
#　2) T-Message の作成
def createTransactionalMessage(token):
    url = restURL + "messaging/v1/email/definitions"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {
            "definitionKey": defkey,
            "status": "Active",
            "name": msgName,
            "description": "Created Via API",
            "classification": "Default Transactional",
            "content": {
              "customerKey": emailCustomerKey
            },
            "subscriptions": {
              "list": listExternalKey,
              "autoAddSubscriber": True,
              "updateSubscriber": True
            }
      }  
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   resInJson
 
# 3) T-Message の送信                
def sendTransactionalMessage(token, defkey):
    url = restURL + "messaging/v1/email/messages/" + "".join(random.choices(string.ascii_letters + string.digits, k=32))
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {
              "definitionKey": defkey,
              "recipient":
              {
              "contactKey": contactKey,
                "to": email
              }
      }  
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   resInJson
 
# 4) メッセージ送信の完了                
def sendTransactionalMessage(token, defkey):
    url = restURL + "messaging/v1/email/messages/" + "".join(random.choices(string.ascii_letters + string.digits, k=32))
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {
              "definitionKey": defkey,
              "recipient":
              {
              "contactKey": contactKey,
                "to": email
              }
      }  
 
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers, method="POST")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    return   resInJson
 
def checkStatus(token, messageKey):
    url = restURL + "messaging/v1/email/messages/" + messageKey
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {}
 
    # 実行 
    req = urllib.request.Request(url, data,  headers, method="GET")  
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode("utf-8"))  
    print(resInJson["eventCategoryType"])
    startTime =  time.time()
    returnCode = 0
 
    # メッセージの送信が完了するまで繰り返す
    while resInJson["eventCategoryType"] != "TransactionalSendEvents.EmailSent":
      print("メッセージの送信処理中・・・ステータス：" + resInJson["eventCategoryType"])
      req = urllib.request.Request(url, data,  headers, method="GET")  
      response = urllib.request.urlopen(req).read()
      resInJson = json.loads(response.decode("utf-8"))  
      time.sleep(10)
 
      # 3分待っても送信ステータスが完了にならないのなら、やめる
      if time.time() - startTime > 180 : 
        print("タイムアウトです")
        returnCode = 1
        break
        
    if returnCode == 0:    
      print("送信完了しました")
    elif returnCode == 1 :
      print("送信ステータスチェックがタイムアウトしました")
    else :
      print("未定義のエラーです")
 
### 実処理　####
# トークン取得
res = getAuthentication()
# メッセージ送信と状態取得
createMessageResponse = createTransactionalMessage(res["access_token"])
sendMessageResponse = sendTransactionalMessage(res["access_token"], createMessageResponse["definitionKey"])
checkMessageStatus = checkStatus(res["access_token"], sendMessageResponse["responses"][0]["messageKey"])
 

