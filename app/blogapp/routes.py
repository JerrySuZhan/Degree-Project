from sqlalchemy import or_, and_
from blogapp import app, db, models
from flask import Flask, render_template, request, session, redirect, url_for
from blogapp.config import Config
from blogapp.models import Buildings
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
from blogapp.forms import search_buildings, search_conditions

app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # root用户名123456密码 test数据库

db.__init__(app)


@app.route('/')
@app.route('/index')
def index():
    session['name'] = ""
    session['district'] = ""
    session['bedrooms'] = ""
    session['livingrooms'] = ""
    session['price_per_meter'] = ""
    return render_template('index.html')


@app.route('/listing/<int:page><string:name><string:district><string:bedrooms><string:livingrooms><string:price_per_meter>',
           methods=['post', 'get'])
def listing(page=None, name=None, district=None, bedrooms=None, livingrooms=None, price_per_meter=None):
    print("成功1")
    if not page:
        page = 1
    if not name:
        name = 'null'
    if not district:
        district = 'null'
    if not bedrooms:
        bedrooms = 'null'
    if not livingrooms:
        livingrooms = 'null'
    if not price_per_meter:
        price_per_meter = 'null'

    if request.method == 'POST':
        search_input = request.form.get('content')  # 需要查询的内容
        district_input = request.form.get('district')
        bedrooms_input = request.form.get('bedrooms')
        livingrooms_input = request.form.get('livingrooms')
        price_per_meter_input = request.form.get('price_per_meter')

        session['name'] = search_input
        session['district'] = district_input
        session['bedrooms'] = bedrooms_input
        session['livingrooms'] = livingrooms_input
        session['price_per_meter'] = price_per_meter_input
        # if search_input is None:
        #     search_input = ""
        #     session['name'] = search_input
        # if district_input is None or district_input == "Any":
        #     district_input = ""
        #     session['district'] = district_input
        # if bedrooms_input is None or bedrooms_input == "Any":
        #     bedrooms_input = ""
        #     session['bedrooms'] = bedrooms_input
        # if livingrooms_input is None or livingrooms_input == "Any":
        #     livingrooms_input = ""
        #     session['livingrooms'] = livingrooms_input

        if search_input is None or search_input == "Any" or search_input == "":
            search_input = ""
            session['name'] = search_input
        if district_input is None or district_input == "Any" or district_input == "":
            district_input = ""
            session['district'] = district_input
        if bedrooms_input is None or bedrooms_input == "Any" or bedrooms_input == "":
            bedrooms_input = ""
            session['bedrooms'] = bedrooms_input
        if livingrooms_input is None or livingrooms_input == "Any" or livingrooms_input == "":
            livingrooms_input = ""
            session['livingrooms'] = livingrooms_input
        if price_per_meter_input is None or price_per_meter_input == "Any" or price_per_meter_input == "":
            price_per_meter_input = ""
            session['price_per_meter'] = price_per_meter_input


        print("name1: " + session['name'])
        print("district1: " + session['district'])
        print("bedrooms1: " + session['bedrooms'])
        print("livingrooms1: " + session['livingrooms'])
        print("price_per_meter1: " + session['price_per_meter'])

        u = Buildings.query.filter(and_
            (
            or_(
                Buildings.district.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.address.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.total_price.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.price_per_meter.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.build_time.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.num_of_bedrooms.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.num_of_living_rooms.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.size.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.orientation.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.building_type.like("%" + search_input + "%") if search_input is not None else "",
                Buildings.num_of_floors.like("%" + search_input + "%") if search_input is not None else ""
            ),
            and_(
                Buildings.district.like("%" + district_input + "%") if district_input is not None else "",
                Buildings.num_of_bedrooms.like("%" + bedrooms_input + "%") if bedrooms_input is not None else "",
                Buildings.num_of_living_rooms.like("%" + livingrooms_input + "%") if livingrooms_input is not None else "",
                # Buildings.price_per_meter.like("%" + price_per_meter_input + "%") if price_per_meter_input is not None else ""
        )
        )
        )
        u = u.paginate(page=page, per_page=18)
        # print("search成功")

        if search_input == "":
            search_input = 'null'
        if district_input == "":
            district_input = 'null'
        if bedrooms_input == "":
            bedrooms_input = 'null'
        if livingrooms_input == "":
            livingrooms_input = 'null'
        if price_per_meter_input == "":
            price_per_meter_input = 'null'

        return render_template('listing.html', u=u.items, pagination=u, search_input=search_input,
                               district_input=district_input,
                               bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input, price_per_meter_input=price_per_meter_input)

    else:
        print("成功2")
        if session['name'] == "" and session['district'] == "" and session['bedrooms'] == "" and session['livingrooms'] and session['price_per_meter']== "":
            print("name: " + session['name'])
            print("district: " + session['district'])
            print("bedrooms: " + session['bedrooms'])
            print("livingrooms: " + session['livingrooms'])
            print("price_per_meter: " + session['price_per_meter'])
            search_input = 'null'
            district_input = 'null'
            bedrooms_input = 'null'
            livingrooms_input = 'null'
            price_per_meter_input = 'null'
            u = Buildings.query.paginate(page=page, per_page=18)
        else:
            search_input = session['name']
            district_input = session['district']
            bedrooms_input = session['bedrooms']
            livingrooms_input = session['livingrooms']
            price_per_meter_input = session['price_per_meter']
            # if session['name'] == "":
            #     search_input = ""
            # if session['district'] == "":
            #     district_input = ""
            # if session['bedrooms'] == "":
            #     bedrooms_input = ""
            # if session['livingrooms'] == "":
            #     livingrooms_input = ""

            print("name2: " + session['name'])
            print("district2: " + session['district'])
            print("bedrooms2: " + session['bedrooms'])
            print("livingrooms2: " + session['livingrooms'])
            print("price_per_meter: " + session['price_per_meter'])

            u = Buildings.query.filter(and_
                (
                or_(
                    Buildings.district.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.address.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.total_price.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.price_per_meter.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.build_time.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.num_of_bedrooms.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.num_of_living_rooms.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.size.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.orientation.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.building_type.like("%" + search_input + "%") if search_input is not None else "",
                    Buildings.num_of_floors.like("%" + search_input + "%") if search_input is not None else ""
                ),
                and_(
                    Buildings.district.like("%" + district_input + "%") if district_input is not None else "",
                    Buildings.num_of_bedrooms.like("%" + bedrooms_input + "%") if bedrooms_input is not None else "",
                    Buildings.num_of_living_rooms.like("%" + livingrooms_input + "%") if livingrooms_input is not None else "",
                    # Buildings.price_per_meter.like("%" + price_per_meter_input + "%") if price_per_meter_input is not None else ""
                )
            )
            )
            u = u.paginate(page=page, per_page=18)

            if search_input == "":
                search_input = 'null'
            if district_input == "":
                district_input = 'null'
            if bedrooms_input == "":
                bedrooms_input = 'null'
            if livingrooms_input == "":
                livingrooms_input = 'null'
            if price_per_meter_input == "":
                price_per_meter_input = 'null'

        print("未进行search")
        return render_template('listing.html', u=u.items, pagination=u, search_input=search_input,
                               district_input=district_input,
                               bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input, price_per_meter_input=price_per_meter_input)
    return render_template('listing.html')


@app.route('/search', methods=['post', 'get'])
def search():
    search_input = request.form.get('content')  # 需要查询的内容
    if search_input is None:
        search_input = " "
    contents = search_input.split()
    quotes = []
    for content in contents:
        # 查询跟content有关的数据，返回结果为列表
        quote = Buildings.query.filter(or_(
            Buildings.district.like("%" + content + "%") if content is not None else "",
            Buildings.address.like("%" + content + "%") if content is not None else "",
            Buildings.total_price.like("%" + content + "%") if content is not None else "",
            Buildings.price_per_meter.like("%" + content + "%") if content is not None else "",
            Buildings.build_time.like("%" + content + "%") if content is not None else "",
            Buildings.num_of_bedrooms.like("%" + content + "%") if content is not None else "",
            Buildings.num_of_living_rooms.like("%" + content + "%") if content is not None else "",
            Buildings.size.like("%" + content + "%") if content is not None else "",
            Buildings.orientation.like("%" + content + "%") if content is not None else "",
            Buildings.building_type.like("%" + content + "%") if content is not None else "",
            Buildings.num_of_floors.like("%" + content + "%") if content is not None else ""
        )).all()
        quotes = list(set(quotes) | set(quote))  # 取并集
        # quotes = list(set(quotes) & set(quote))  # 取交集
    return render_template('search.html', quotes=quotes)  # 将查询结果返回到前端


@app.route('/test')
def test():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 3))
    paginate = Buildings.query.paginate(page, per_page, error_out=False)
    stus = paginate.items
    return render_template('test.html', paginate=paginate, stus=stus)


@app.route('/single')
def single():
    return render_template('single-property.html')


@app.route('/new')
def new():
    return render_template('post.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


if __name__ == '__main__':
    app.run(debug=True)

    # conn = pymysql.connect(host='127.0.0.1', user='root', password='0806', port=3306, db='house_small')
    # cur = conn.cursor()
    # sql = "SELECT `地区`, `地址` , `总价` , `单价` , `建造时间` , `卧室数` , `客厅数` , `大小` , `朝向` , `楼层类型` , `总层数` FROM `house_small` WHERE 1"
    # cur.execute(sql)
    # u = cur.fetchall()
    # conn.close()
