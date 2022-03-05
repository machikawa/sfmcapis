# sfmcapis

MCのRestAPIを実行するPythonのプログラムです。
ご自身の端末にてPythonが実行可能ならば、ターミナルやPowershellから下記のようにプログラムを実行できるはずです。
どのプログラムも引数は不要です。

　　_python filename.py_

  
# ざっくりしたつかいかた

詳細は各ファイルの "### 準備 ###" セクションに書いてあります
おおよそ、" ### 定数 ###" という部分に、ご自身の ClientID/Secret 等を埋め込むことになります。
ClientID/Secret などは別のクラスにしたかったのですが、都度埋め込んであります。

# ファイルの説明


  CreateAndSendTransactionalMessage.py
  
  トランザクショナルメッセージングAPIでメッセージ定義を作り、送信します
  
  PushMessageCreateAndSend.py
  PushMessageCreation.py
  PushMessageSend.py
  
  Pushメッセージ系のAPIです。メッセージ作成と送信を同時に行うもの。作成および送信を個別に行うもののそれぞれ3つ。

  insertAndCheckDEInsertion.py
  DEinsertAuto.py
  
  DEへのインサートを行います。Asyncで行います。
  前者はTSEに対応しておらず、古いパッケージなのでほぼ使えませんが、
  例外処理やリトライなどが入っているので、そのまま残しておあります。
  
