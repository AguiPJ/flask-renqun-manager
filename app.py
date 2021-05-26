import random
from os.path import abspath

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

from routers.receive import receive_opt
from utils import randomData, randomDataStart, randomDataEnd, getTime

# 注册flask app，路由蓝图以及解决跨域问题
app = Flask(__name__, template_folder="dist")
app.register_blueprint(blueprint=receive_opt, url_prefix='/jieshou')
CORS(app, resources={r"/*": {"origins": "*"}})


# 前端静态文件
@app.route('/', methods=['GET'])
def Home(): return render_template('index.html')


@app.route('/css/<file>', methods=['GET'])
def staticCss(file): return send_from_directory(abspath(f"dist/css"), file, as_attachment=True)


@app.route('/js/<file>', methods=['GET'])
def staticJs(file): return send_from_directory(abspath(f"dist/js"), file, as_attachment=True)


@app.route('/img/<file>', methods=['GET'])
def staticImg(file): return send_from_directory(abspath(f"dist/img"), file, as_attachment=True)


@app.route('/fonts/<file>', methods=['GET'])
def staticFonts(file): return send_from_directory(abspath(f"dist/fonts"), file, as_attachment=True)


series = [
    {"name": "致远楼", "data": randomData()},
    {"name": "春熙路", "data": randomData()},
    {"name": "长白山", "data": randomData()},
]


@app.get('/statistics')
def statistics():
    # 生成随机数模拟监控人数

    ct = getTime()
    timeList = [(ct + i * 2000) for i in range(10)]
    for item in series:
        del item["data"][0]
        item["data"].append(random.randrange(randomDataStart, randomDataEnd))
    return {'data': {
        "times": timeList,
        "series": series
    }}


if __name__ == '__main__':
    app.run("0.0.0.0", port=7000, debug=True)
