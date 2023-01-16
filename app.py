# flask import 하는 부분
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# pymongo import 하는 부분
from pymongo import MongoClient

# bs4 import 하는 부분
from bs4 import BeautifulSoup

# Certifi import 하는 부분 (Port 5000을 사용하기 위해서)
import certifi

ca = certifi.where()

# request import 하는 부분
import requests

# MongoDB client, db 변수 선언
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.idr3zpp.mongodb.net/Cluster0?retryWrites=true&w=majority',
    tlsCAFile=ca)
db = client.dbsparta

img_result_dic = {
    '1': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon01.png',
    '2': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon06.png',
    '3': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon04.png',
    '4': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon05.png',
    '5': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon07.png',
    '6': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon08.png',
    '7': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon02.png',
    '8': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon03.png',
    '9': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon09.png',
    '10': 'http://spartacodingclub.shop/static/images/rtans/SpartaIcon10.png'
}

@app.route('/')
def home():
    return render_template('index.html')


## 닉네임 저장
@app.route("/api/name", methods=["POST"])
def name_init():
    # user 의 닉네임을 받아옵니다.
    name_receive = request.form['name_give']

    # user의 닉네임이 중복인지 확인합니다.
    users_list = list(db.users.find({}, {'_id': False}))
    for user in users_list:
        if name_receive == user.get('name'):
            return jsonify({'msg': '중복입니다!'})

    ## Result 값 0으로 init
    result_receive = 0;

    ## url 값 임의의 url 값으로 init
    url_receive = ''

    ## result_list 값 0으로 init
    result_list_receive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    doc = {
        'name': name_receive,
        'result': result_receive,
        'image': url_receive,
        'result_list': result_list_receive
    }

    db.users.insert_one(doc)

    return jsonify({'msg': '닉네임 등록 완료!'})


## 결과값을 질문지 하나하나마다 할때 post API 실행
@app.route("/api/answer", methods=["POST"])
def answer_post():
    # 숫자 하나만 넘겨주는 경우
    answer_receive = request.form['answer_give']
    name_receive = request.form['name_give']

    # users_list = list(db.users.find({}, {'_id': False}))
    # # result_list = users_list.get('result_list')
    result_list = db.users.find_one({'name': name_receive}, {'_id': False}, {'result': False}, {'image': False},
                                    {'name': False})
    # result_list = {'result_list' : [0 ,1, 2, 3, 1, ...]}

    result_list = result_list['result_list']

    # for user in users_list:
    if answer_receive == 1:
        result_list[0] += 1;
        result_list[3] += 1;
        result_list[5] += 1;
        db.users.update_one({'name': name_receive}, {'$set': {'result_list': result_list}})

    if answer_receive == 2:
        result_list[4] += 1;
        result_list[6] += 1;
        result_list[7] += 1;
        db.users.update_one({'name': name_receive}, {'$set': {'result_list': result_list}})

    if answer_receive == 3:
        result_list[1] += 1;
        result_list[2] += 1;
        result_list[8] += 1;
        result_list[9] += 1;
        db.users.update_one({'name': name_receive}, {'$set': {'result_list': result_list}})


## 결과물 보여주기
@app.route("/api/result", methods=["POST"])
def result_update():
    ## result 의 값을 0에서  최댓값 (result_list[max]) 으로 바꾸기
    name_receive = request.form['name_give']
    users_list = list(db.users.find({}, {'_id': False}))
    result_list = users_list.get('result_list')

    ## result Update
    for user in users_list:
        if name_receive == user.get('name'):
            db.users.update_one({'name': name_receive}, {'$set': {'result': result_list[max]}})

    ## image Url Update
    url_list = img_result_dic['result_list[max]']
    db.users.update_one({'name': name_receive}, {'$set': {'image': url_list}})

    # for user in users_list:
    #     if name_receive == user.get('name'):
    #         img_url = users_list.get('image')
    # 다음과 같이 for 문을 쓰는 것 대신에 find_one을 사용함.
    img_url = db.users.find_one({'name': name_receive}, {'_id': False}, {'result': False}, {'result_list': False},
                                {'name': False})
    img_url = img_url['image']
    return jsonify({'img_url': img_url})


## 내 결과 다시보기
@app.route("/api/re_result", methods=["POST"])
def result_get():
    name_receive = request.form['name_give']
    users_list = list(db.users.find({}, {'_id': False}))
    # for user in users_list:
    #     if name_receive == user.get('name'):
    #         img_url = users_list.get('image')
    img_url = db.users.find_one({'name': name_receive}, {'_id': False}, {'result': False}, {'result_list': False},
                                {'name': False})
    img_url = img_url['image']

    return jsonify({'img_url': img_url})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
