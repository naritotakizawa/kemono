======
kemono
======

Djangoで、けものフレンズのキャラを認識させる（Deep Learning）
https://torina.top/main/335/

Python3.5で動作を確認

クイックスタート
-----------

1. プロジェクトをクローンする `git clone https://github.com/naritotakizawa/kemono.git`

2. `pip install -r requirements.txt` opencvが入らない場合は http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv からwhlをダウンロード

3. `python manage.py migrate`

4. `python manage.py runserver`

5. http://127.0.0.1:8000 にアクセスし、画像をアップロードして遊ぶ