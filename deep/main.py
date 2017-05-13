import io
from django.core.files.uploadedfile import InMemoryUploadedFile

import cv2
import numpy as np
from PIL import Image
from .simple_convnet import SimpleConvNet

# ネットワークのインスタンス化と、重みの読み込み
network = SimpleConvNet(
    input_dim=(3, 100, 100), hidden_size=50, output_size=10)
network.load_params('params.pkl')

# 推論の結果となる配列。画像がサーバルなら0って帰る
labels = np.array(['サーバル', 'かばんちゃん', 'かば', 'かわうそ', 'ジャガー',
                   'トキ', 'アライ', 'フェネック', 'すなねこ', 'つちのこ'])


def detect(image):
    """画像を受け取り、顔部分を白線で囲み、顔部分を全て返す"""

    cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

    return [cv2.resize(image[y:y+h, x:x+w], (100, 100)) for x, y, w, h in faces]


def predict(upload_file):
    """推論した結果の画像と内容を返す"""

    # 画像をnumpy配列に
    image_array = np.asarray(Image.open(upload_file))

    # 画像の顔部分が帰ってくる
    faces = detect(image_array)

    # 顔が検出できなかった
    if not faces:
        return upload_file, '誰も検出できませんでした'

    # 顔の格納されたリストをnumpy変換し、形を整え
    faces_array = np.array(faces).reshape(
        (len(faces), 3, 100, 100))

    # 推論
    result = network.predict(faces_array).argmax(axis=1)

    # 映っているキャラクターの名前
    char_names = labels[result]

    # 画像のnumpy配列を、PilowのImageオブジェクトへ
    image = Image.fromarray(np.uint8(image_array))

    # Imageオブジェクトを、Djangoのファイルっぽいオブジェクトへ治す処理
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_file = InMemoryUploadedFile(image_io, None, 'foo.jpg', 'image/jpeg',
                                      image_io.getbuffer().nbytes, None)

    return image_file, ','.join(char_names)
