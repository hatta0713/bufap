# bufap

## bufap は Buffalo製の法人無線LANアクセスポイントWAPMシリーズを管理するためのツールおよびクラスです。

## コマンドラインツールの使い方

bufap-cli

### インストール

### 使用方法
```text
usage: bufap-cli.py [-h] (--get-conf | --read-conf | --wireless-monitor | --client-monitor) [--host HOST] [--username USERNAME] [--password PASSWORD]
                    [--infile INFILE] [--outfile OUTFILE] [--summarize {yes,no}] [--column {user,default}] [--format {raw,text,dict,csv}]

WAPMシリーズコンフィグツール

options:
  -h, --help            show this help message and exit
  --get-conf            設定を取得
  --read-conf           設定を読み込み
  --wireless-monitor    無線環境モニター
  --client-monitor      クライアントモニター
  --host HOST           ホストアドレス(IP)
  --username USERNAME   ユーザー名
  --password PASSWORD   パスワード
  --infile INFILE       設定ファイルのパス
  --outfile OUTFILE     出力先ファイルのパス
  --summarize {yes,no}  ユーザーが変更した部分のみ表示する
  --column {user,default}
  --format {raw,text,dict,csv}
```