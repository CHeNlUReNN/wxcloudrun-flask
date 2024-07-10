# 创建应用实例
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from random import randint
from wxcloudrun import app

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/login0', methods=['POST'])
def logi0():
    if request.method == "POST":
        head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}
        response = requests.get("http://wxxcxtest1.viphk.nnhk.cc", headers=head)
        if response.ok:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            results = soup.findAll("tr")
            for result in results:
                data = result.findAll("td")
                if request.form.get("username") == data[0].getText() and request.form.get("password") == data[1].getText():
                    return jsonify(1)
            return jsonify(0)


@app.route('/login1', methods=['POST'])
def logi():
    if request.method == "POST":
        head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}
        response = requests.get("http://wxxcxtest1.viphk.nnhk.cc", headers=head)
        if response.ok:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            results = soup.findAll("tr")
            for result in results[1:]:
                data = result.findAll("td")
                if request.form.get("username") == data[1].getText() and request.form.get("password") == data[2].getText():
                    tname = data[0].getText()
                    break
            response = requests.get("http://wxxcxtest.free.idcfengye.com/", headers=head)
            if response.ok:
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
                results = soup.findAll("tr")
                rows = []
                for result in results:
                    data = result.findAll("td")
                    if tname == data[5].getText() and data[3].getText() not in rows:
                        rows.append(data[3].getText())
                return jsonify(rows)



@app.route('/dm', methods=['POST'])
def r_d():
    if request.method == "POST":
        head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}
        response = requests.get("http://wxxcxtest.free.idcfengye.com/", headers=head)
        if response.ok:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            results = soup.findAll("tr")
            rows = []
            for result in results:
                data = result.findAll("td")
                id = data[0].getText()
                name = data[2].getText()
                institute = data[3].getText()
                lesson = data[4].getText()
                tid = data[5].getText()
                tname = data[6].getText()
                img = data[1].find("img")
                pho = img["src"]
                rows.append([id, name, institute, lesson, tid, tname,pho])
            #req_data = request.get_json()
            lesson = []
            data = request.json  # 假设请求是 JSON 格式
            for value in data.items():
                if value not in lesson:
                    lesson.append(value)
            index = []  # 存储rows下标
            i = -1
            for info in rows:
                i += 1
                if info[3] in lesson:
                    index.append(i)
            stu = rows[index[randint(0, len(index) - 1)]]
            return jsonify([stu[1],stu[6]])

        else:
            print("fail to obtain info")

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
