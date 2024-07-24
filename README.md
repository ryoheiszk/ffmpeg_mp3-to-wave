# MP3ファイルをWAVファイル(16bit, 16kHz, モノラル)に変換するプログラム

1. `.env`を作成し、ASRのエンドポイントを記載する。

```env
ASR_URL=https://...
```

1. `/input/`にmp3ファイルを入れる。

1. `settings.py`を調整する。

    - `ENABLE_SPLIT`: 分割を有効化する。
    - `SPLIT_DURATION`: 例えば、600とすると、35分の音声ファイルは、10分、10分、10分、5分と分割される。

1. コンテナを起動する。

    ```bash
    docker-compose up --build
    ```

1. 音声は`/output/`に、文字起こしは`/asr/`に出力される。
