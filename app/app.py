from flask import Flask, render_template, request
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/listing')
def listing():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='0806', port=3306, db='house_small')
    cur = conn.cursor()
    sql = "SELECT `地区`, `地址` , `总价` , `单价` , `建造时间` , `卧室数` , `客厅数` , `大小` , `朝向` , `楼层类型` , `总层数` FROM `house_small` WHERE 1"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('listing.html', u=u)


@app.route('/single')
def single():
    return render_template('single-property-1.html')


@app.route('/new')
def new():
    return render_template('post.html')


@app.route('/login')
def login():
    return render_template('login-1.html')


@app.route('/signup')
def signup():
    return render_template('signup-1.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/test')
def test():
  conn = pymysql.connect(host='127.0.0.1', user='root', password='0806', port=3306, db='house')
  cur = conn.cursor()
  sql = "SELECT `地区`, `地址` , `总价` , `单价` , `建造时间` , `卧室数` , `客厅数` , `大小` , `朝向` , `楼层类型` , `总层数` FROM `house` WHERE 1"
  cur.execute(sql)
  u = cur.fetchall()
  conn.close()
  return render_template('test.html',u=u)



if __name__ == '__main__':
    app.run()
