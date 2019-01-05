from app import app
from keras.models import Sequential, load_model
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation,Dropout,Flatten,Dense
from keras.utils import np_utils
import numpy as np
import keras
from PIL import Image
import sys
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

print("現在のディレクトリ: ", os.getcwd())

classes=["安倍晋三","山口那津男","枝野幸男","玉木雄一郎","志位和夫","松井一郎",
"小沢一郎","松沢成文","又市征治","中野正志"]
num_classes=len(classes)
image_size=50

UPLOAD_FOLDER='app/uploads'
ALLOWED_EXTENSIONS=set(['png','jpg','gif'])

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.debug=True

def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    global classes
    if request.method=='POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            #redirect（）でリダイレクト先に行く。リクエストしたURL(ファイルをアップロードするページ）
            return redirect(request.url)
        #ファイルがある場合は次に進める
        file=request.files['file']
        #もしこれが空だったら
        if file.filename=='':
            #flashでメッセージ
            flash('ファイルがありません')
            return redirect(request.url)
        #ファイルが存在し、先ほどのチェックをするallowed_fileがあれば
        if file and allowed_file(file.filename):
            #secure_filenameのファンクションを使ってテェック
            filename=secure_filename(file.filename)
            #os.path.join（）で二つの文字列を連結させて一つの文字列にする
            #ここではフォルダ名とファイル名を連結
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #⑨ファイルパスを変数に格納
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            #⑩モデルのロード[predict.pyからコピー]
            print("-"*10, "filepath: ", filepath)
            #model = load_model('app/traning_model/model.h5')
            model = load_model('app/traning_model/newest_model2.h5')

            print("*"*20, "モデルを読み込みました")
            #(11)NumPy配列に変換[predict.pyからコピー]open()の引数だけfilepathに
            image=Image.open(filepath)
            print("*"*20, image)
            #RGBに変換
            image=image.convert('RGB')
            #画像のサイズを揃える
            image=image.resize((image_size,image_size))
            #でーたをnumpyの数字の列として変換
            data=np.asarray(image)
            #データを初期化
            X=[]
            #Xのリストの一番後ろに追加
            X.append(data)
            #Xをnumppyのarrayとして整える
            X=np.array(X)
            #(12)推定結果[predict.pyからコピー]
            #推定結果を格納する変数を宣言し、モデルにpredictでデータを与える
            result=model.predict([X])[0]
            #推定値を得るために、argmax()で配列の中で一番推定値の高いものを取り出す
            predicted=result.argmax()
            #確率とラベル名を表示していくコードを書く
            percentage=int(result[predicted]*100)
            result_class = classes[predicted]
            return render_template("result.html", result_class=result_class, result_per=str(percentage)+"%")
