###### ASYNC-DEInsertion - REST API #########
import urllib.request
import json 
import datetime
from urllib.error import URLError, HTTPError
import time
import sys

##### 定数 #####
# DE 
deExternalKey = "PLEASE INSERT YOUR DE EXTERNALKEY" # DE の外部キーを入
columnArray = ["Contact","Name","Email"] #DEの列名を列挙する
valueArray = ["PythonSubs","たうんりばー","pyuser"] #基本となるDEの行データ　
# パッケージ
clientID = 'PLEASE INSERT YOUR v1 Legacy ClientID' # 秘密の情報
clientSecret = 'PLEASE INSERT YOUR v1 Legacy ClientSecret' # 秘密の情報
# 附帯情報
domain = "PleaseInsertYourTesetingEmailDomain.co.jp" # テスト用のEmailドメイン。Emailの項目に使う
rowsInserting = 300 # 何レコード追加するか。　だいたい一万前後でガタがくる
retryTimer = [20,60,120] #API リトライの間隔。単位は秒 
### リトライはお作法です###

##### 初期化 #####
responseBody = []
requestBody = []

#### Methods ####
# 1) 認証トークンの取得@v1
def getAuthentication():
    # HTTP リクエスト定義
    url = 'https://auth.exacttargetapis.com/v1/requestToken'
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = {
        'clientId': clientID ,
        'clientSecret':clientSecret
    }  
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='POST')    
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode('utf-8'))  
    return resInJson


#　2) DEへインサートするリクエストを行う
def renInsert(token,bodyobj):
    # HTTP リクエスト定義
    Auth =  "'Authorization'" + " : " + "'Bearer " +   token + "'"
    url = 'https://www.exacttargetapis.com/data/v1/async/dataextensions/key:' + deExternalKey + '/rows'
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {"items":bodyobj}
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='POST')    
    res = invokeHTTPRequest(req,"インサート")
    # リトライの仕組み。
    if res == "1":
        retryCount = 0
        while retryCount < len(retryTimer):
            print(str(retryCount+1) + "回目のリトライです。　" + str(retryTimer[retryCount]) + "秒待機します")
            time.sleep(retryTimer[retryCount])
            resRetry = invokeHTTPRequest(req,"インサート")
            retryCount += 1
            # リトライ上限に達したらExitする
            if retryCount == len(retryTimer):
                print("タイムアウトの上限に達しました")
                sys.exit(1)
    #記録
    print("HTTPStatusCode="+str(res.code))
    return res

                
def invokeHTTPRequest(req,actionName):
    try:
        print(actionName+"開始:"+str(datetime.datetime.now()))
        res = urllib.request.urlopen(req)
    except HTTPError as e:
        print('ダメです（HTTPエラーです😭　下のコードを確認してください）')
        print('Error code: ', e.code)
        return "1"
    except URLError as e:
        print('ダメです（We failed to reach a server.話にならんな）')
        print('Reason: ', e.reason)  
        return "99"
    print(actionName+"終了:"+str(datetime.datetime.now()))
    return res

# BODY 部を作成する。
def createBody3(colAr,valAr,rowsInserting):
    # 配列チェッカー
    if len(colAr) == len(valAr):
        print("OK")
    else :
        return "ダメです(定数部のcolumnArrayとvalueArrayの配列の長さが異なっているので見直してください)"

    # Body 部の生成
    additives = 1 # 末尾にインクリする数字
    for i in range(rowsInserting):
        row = {}    
        idx = 0  
        for col in colAr :
            if col == "Email" :
                row[col] = valAr[idx] + str(additives) + "@" + domain
            else :
                row[col] = valAr[idx] + str(additives)
            idx += 1  
        requestBody.append(row)
        additives += 1
    return requestBody
    
def checkStatus(token,reqId2):
    # HTTP リクエスト定義
    Auth =  "'Authorization'" + " : " + "'Bearer " +   token + "'"
    url = 'https://www.exacttargetapis.com/data/v1/async/' + reqId2 + '/results'
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token
    }
    data = {}
    # 実行 
    req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='GET')   
    response = urllib.request.urlopen(req).read()
    resInJson = json.loads(response.decode('utf-8'))
    return resInJson

def checkInsertResult(resResult,reqId3):
    resDict = resResult["items"]
    i = 0
    okeyCnt = 0
    ngCnt = 0
    for res in resDict:
        stsCode = resDict[i]["status"]
        if stsCode == "OK":
            okeyCnt += 1
        else :
            ngCnt += 1    
        i += 1 
    print("リクエストID:" + reqId3+" の結果は" )
    print(str(okeyCnt)+"件成功："+ str(ngCnt)+ "件失敗")
    return okeyCnt
        
### 実処理　####
# トークン取得
res = getAuthentication()
# 大規模データインサート
response = renInsert(res["accessToken"],createBody3(columnArray,valueArray,rowsInserting))
## MEMO - stetus code は response.code, リクエストIDは　responseBody['requestId']

# ダサいけどリクエストID取得
print("レスポンス："+str(response.code))
textResponse = response.read().decode('utf-8')
dictResponse = json.loads(textResponse)
reqId = dictResponse["requestId"]

# ステータスチェック処理
resResult = checkStatus(res["accessToken"],reqId)
# 何件のレコードが入ったかな。
print("### AsyncChecker ###")
okCnt = checkInsertResult(resResult, reqId)

while okCnt != rowsInserting:
    resResult = checkStatus(res["accessToken"],reqId)
    # 何件のレコードが入ったかな。
    print("### AsyncChecker ###")
    okCnt = checkInsertResult(resResult, reqId)
    if okCnt == rowsInserting :
        print("インサート非同期処理終了時刻"+str(datetime.datetime.now()))
    else:
        time.sleep(3)

