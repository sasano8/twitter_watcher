# twitte_watcher
指定したユーザーの最新ツイートを監視し、ラインに通知する。

# Requirement

- Python 3.8+

# Installation

``` shell
```

# Getting started

1. 環境変数の設定
    本ライブラリを使用するには、次の環境変数の設定が必要（`.env`でのみ動作確認）です。

    - TWITTER_API_KEY
    - TWITTER_API_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN

2. スクリーンネーム指定し監視を初めます

    - interval: データ取得の間隔を秒で指定します（サーバに負荷をかけすぎない間隔にしてください）
    - screen_names: 指定した複数のスクリーンネームを監視します

``` shell
python3 -m twitter_watcher --interval 10 <screen_names>
```

# Setup


# 開発ガイド
CONTRIBUTING.mdを参照ください。

