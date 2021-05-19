import base64
import os
import pickle

from sqlalchemy import or_, and_
from werkzeug.security import check_password_hash, generate_password_hash
from blogapp import app, db, models, mail
from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response, jsonify
from flask_babel import Babel, gettext as _
from blogapp.config import Config
#from blogapp.embedding import Embedding
#from blogapp.embedding2 import Embedding2
from blogapp.embedding_manager import EmbeddingManager
from blogapp.house_info import HouseInfo
from blogapp.models import Buildings, User, Message, Ratings
from blogapp.forms import search_buildings, search_conditions, LoginForm, SignupForm, ProfileForm, \
    ChangePasswordForm, AddHouseForm, SendEmailForm, VerifyAndResetForm, SingleForm, EditForm
from flask_mail import Message
import random
import string
import time

# app = Flask(__name__)
# app.config.from_object(Config)
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # root用户名123456密码 test数据库
# db.__init__(app)
from blogapp.user_rating import UserRating

model = pickle.load(open('model.pkl', 'rb'))

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

@babel.localeselector
def get_locale():
    cookie = request.cookies.get('locale')
    if cookie in ['zh', 'en']:
        return cookie
    return request.accept_languages.best_match(app.config.get('BABEL_DEFAULT_LOCALE'))  # 没有cookie时，默认为 en

@app.route('/set_locale/<locale>') # 用ajax请求来设置cookie
def set_locale(locale):
    response = make_response(jsonify(message='update success'))
    if locale:
        response.set_cookie('locale', locale, 60 * 60)
        return response


@app.route('/')
@app.route('/index')
def index():
    user = {'username': ' '}
    session['name'] = ""
    session['district'] = ""
    session['bedrooms'] = ""
    session['livingrooms'] = ""
    session['price_per_meter'] = ""
    session['building_type'] = ""
    session['size'] = ""
    session['order'] = ""

    session['input' ] = ""

    if not session.get("LOGING_USER") is None:
        user = User.query.filter(User.id == session.get("LOGING_USER")['userid']).first()
        user_id = user.id
    else:
        user_id = 1

    # 1. 获取该用户的embedding
    user_embedding_str = mgr_user_embedding.get_embedding(user_id)
    # 2. 获取该用户看过的电影ID列表
    watch_ids = obj_user_rating.get_user_watched_ids(user_id)
    # 3. 使用近邻搜索获取用户可能喜欢的电影ID列表
    target_user_ids = mgr_house_embedding.search_ids_by_embedding(user_embedding_str, 2 * len(watch_ids))
    # 4. 去除已经看过的列表
    target_house_ids = [x for x in target_user_ids if x not in watch_ids]

    house_ids = target_house_ids[0:6]

    similar_property = []
    for i in house_ids:
        result = Buildings.query.filter(Buildings.id == i).first()
        if result is not None:
            similar_property.append(result)

    return render_template('index.html', title='Home', user=user, similar_property=similar_property)


@app.route(
    '/listing/<int:page><string:name><string:district><string:bedrooms><string:livingrooms><string:price_per_meter><string:building_type><string:size>',
    methods=['post', 'get'])
def listing(page=None, name=None, district=None, bedrooms=None, livingrooms=None, price_per_meter=None,
            building_type=None, size=None):
    lower_bond = 0
    upper_bond = 10000000

    size_lower_bond = 0
    size_upper_bond = 10000000

    # 获取Get数据
    order = request.values.get("name")
    if order is not None:
        session['order'] = order

    # 返回
    print(order)

    if not session.get("LOGING_USER") is None:
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
        if not size:
            size = 'null'
        if not building_type:
            building_type = 'null'

        if request.method == 'POST':
            search_input = request.form.get('content')  # 需要查询的内容
            district_input = request.form.get('district')
            bedrooms_input = request.form.get('bedrooms')
            livingrooms_input = request.form.get('livingrooms')
            price_per_meter_input = request.form.get('price_per_meter')
            size_input = request.form.get('size')
            building_type_input = request.form.get('building_type')


            if building_type_input == 'High Floor':
                building_type_input = '高楼层'
            if building_type_input == 'Medium Floor':
                building_type_input = '中楼层'
            if building_type_input == 'Low Floor':
                building_type_input = '低楼层'
            if building_type_input == 'Top Floor':
                building_type_input = '顶层'
            if building_type_input == 'Lowest Floor':
                building_type_input = '底层'
            if building_type_input == 'Ground Floor':
                building_type_input = '地下室'


            if district_input == 'Miyun':
                district_input = '密云'
            if district_input == 'Xicheng':
                district_input = '西城'     
            if district_input == 'Dongcheng':
                district_input = '东城'
            if district_input == 'Haidian':
                district_input = '海淀'
            if district_input == 'Chaoyang':
                district_input = '朝阳'
            if district_input == 'Fengtai':
                district_input = '丰台'
            if district_input == 'Mentougou':
                district_input = '门头沟'
            if district_input == 'Shijingshan':
                district_input = '石景山'
            if district_input == 'Fangshan':
                district_input = '房山'
            if district_input == 'Tongzhou':
                district_input = '通州'
            if district_input == 'Shunyi':
                district_input = '顺义'
            if district_input == 'Changping':
                district_input = '昌平'
            if district_input == 'Daxing':
                district_input = '大兴'
            if district_input == 'Huairou':
                district_input = '怀柔'
            if district_input == 'Pinggu':
                district_input = '平谷'
            if district_input == 'Yanqing':
                district_input = '延庆'



            session['name'] = search_input
            session['district'] = district_input
            session['bedrooms'] = bedrooms_input
            session['livingrooms'] = livingrooms_input
            session['price_per_meter'] = price_per_meter_input
            session['size'] = size_input
            session['building_type'] = building_type_input

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
            if size_input is None or size_input == "Any" or size_input == "":
                size_input = ""
                session['size'] = size_input
            if building_type_input is None or building_type_input == "Any" or building_type_input == "":
                building_type_input = ""
                session['building_type'] = building_type_input

            # print("name1: " + session['name'])
            # print("district1: " + session['district'])
            # print("bedrooms1: " + session['bedrooms'])
            # print("livingrooms1: " + session['livingrooms'])
            # print("price_per_meter1: " + session['price_per_meter'])
            # print("size: " + session['size'])
            # print("building_type: " + session['building_type'])

            if price_per_meter_input == "10000-20000":
                lower_bond = 10000
                upper_bond = 20000

            if price_per_meter_input == "20000-30000":
                lower_bond = 20000
                upper_bond = 30000

            if price_per_meter_input == "30000-40000":
                lower_bond = 30000
                upper_bond = 40000

            if price_per_meter_input == "40000-50000":
                lower_bond = 40000
                upper_bond = 50000

            if price_per_meter_input == "50000-60000":
                lower_bond = 50000
                upper_bond = 60000

            if price_per_meter_input == "60000-70000":
                lower_bond = 60000
                upper_bond = 70000

            if price_per_meter_input == "70000-80000":
                lower_bond = 70000
                upper_bond = 80000

            if price_per_meter_input == "80000-90000":
                lower_bond = 80000
                upper_bond = 90000

            if price_per_meter_input == ">90000":
                lower_bond = 90000

            # 大小
            if size_input == "0-20":
                size_lower_bond = 0
                size_upper_bond = 20

            if size_input == "20-40":
                size_lower_bond = 20
                size_upper_bond = 40

            if size_input == "40-60":
                size_lower_bond = 40
                size_upper_bond = 60

            if size_input == "60-80":
                size_lower_bond = 60
                size_upper_bond = 80

            if size_input == "80-120":
                size_lower_bond = 80
                size_upper_bond = 100

            if size_input == "120-140":
                size_lower_bond = 100
                size_upper_bond = 120

            if size_input == "140-160":
                size_lower_bond = 120
                size_upper_bond = 140

            if size_input == ">160":
                size_lower_bond = 160

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
                    Buildings.num_of_living_rooms.like(
                        "%" + livingrooms_input + "%") if livingrooms_input is not None else "",
                    Buildings.price_per_meter >= lower_bond if lower_bond is not None else "",
                    Buildings.price_per_meter <= upper_bond if upper_bond is not None else "",
                    Buildings.size >= size_lower_bond if size_lower_bond is not None else "",
                    Buildings.size <= size_upper_bond if size_upper_bond is not None else "",
                    Buildings.building_type.like(
                        "%" + building_type_input + "%") if building_type_input is not None else ""
                    # Buildings.price_per_meter.like("%" + price_per_meter_input + "%") if price_per_meter_input is not None else ""
                )
            )
            )

            if order is not None:
                if order == 'Price (Hi-Lo)':
                    u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                    print("1")

                if order == 'Price (Lo-Hi)':
                    u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                    print("2")

                if order == 'Lowest SqFt':
                    u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                    print("3")

                if order == 'Largest SqFt':
                    u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                    print("4")

            else:
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
            if size_input == "":
                size_input = 'null'
            if building_type_input == "":
                building_type_input = 'null'

            return render_template('listing.html', u=u.items, pagination=u, search_input=search_input,
                                   district_input=district_input,
                                   bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input,
                                   price_per_meter_input=price_per_meter_input, size_input=size_input,
                                   building_type_input=building_type_input)

        else:
            if session['name'] == "" and session['district'] == "" and session['bedrooms'] == "" and session[
                'livingrooms'] and session['price_per_meter'] == "" and session['size'] == "" and session[
                'building_type'] == "":
                # print("name: " + session['name'])
                # print("district: " + session['district'])
                # print("bedrooms: " + session['bedrooms'])
                # print("livingrooms: " + session['livingrooms'])
                # print("price_per_meter: " + session['price_per_meter'])
                # print("size: " + session['size'])
                # print("building_type: " + session['building_type'])

                search_input = 'null'
                district_input = 'null'
                bedrooms_input = 'null'
                livingrooms_input = 'null'
                price_per_meter_input = 'null'
                size_input = 'null'
                building_type_input = 'null'

                if order is None:
                    u = Buildings.query.paginate(page=page, per_page=18)

                else:
                    if order == 'Price (Hi-Lo)':
                        u = Buildings.query.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("1")

                    if order == 'Price (Lo-Hi)':
                        u = Buildings.query.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("2")

                    if order == 'Lowest SqFt':
                        u = Buildings.query.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("3")

                    if order == 'Largest SqFt':
                        u = Buildings.query.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("4")

                return redirect(url_for('index'))

            else:
                search_input = session['name']
                district_input = session['district']
                bedrooms_input = session['bedrooms']
                livingrooms_input = session['livingrooms']
                price_per_meter_input = session['price_per_meter']
                size_input = session['size']
                building_type_input = session['building_type']

                # print("name2: " + session['name'])
                # print("district2: " + session['district'])
                # print("bedrooms2: " + session['bedrooms'])
                # print("livingrooms2: " + session['livingrooms'])
                # print("price_per_meter: " + session['price_per_meter'])
                # print("size: " + session['size'])
                # print("building_type: " + session['building_type'])

                ##每平米价格
                if price_per_meter_input == "10000-20000":
                    lower_bond = 10000
                    upper_bond = 20000

                if price_per_meter_input == "20000-30000":
                    lower_bond = 20000
                    upper_bond = 30000

                if price_per_meter_input == "30000-40000":
                    lower_bond = 30000
                    upper_bond = 40000

                if price_per_meter_input == "40000-50000":
                    lower_bond = 40000
                    upper_bond = 50000

                if price_per_meter_input == "50000-60000":
                    lower_bond = 50000
                    upper_bond = 60000

                if price_per_meter_input == ">60000":
                    lower_bond = 60000

                # 大小
                if size_input == "0-20":
                    size_lower_bond = 0
                    size_upper_bond = 20

                if size_input == "20-40":
                    size_lower_bond = 20
                    size_upper_bond = 40

                if size_input == "40-60":
                    size_lower_bond = 40
                    size_upper_bond = 60

                if size_input == "60-80":
                    size_lower_bond = 60
                    size_upper_bond = 80

                if size_input == "80-120":
                    size_lower_bond = 80
                    size_upper_bond = 100

                if size_input == "120-140":
                    size_lower_bond = 100
                    size_upper_bond = 120

                if size_input == "140-160":
                    size_lower_bond = 120
                    size_upper_bond = 140

                if size_input == ">160":
                    size_lower_bond = 160

                u = Buildings.query.filter(and_
                    (
                    or_(
                        Buildings.district.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.address.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.total_price.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.price_per_meter.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.build_time.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.num_of_bedrooms.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.num_of_living_rooms.like(
                            "%" + search_input + "%") if search_input is not None else "",
                        Buildings.size.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.orientation.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.building_type.like("%" + search_input + "%") if search_input is not None else "",
                        Buildings.num_of_floors.like("%" + search_input + "%") if search_input is not None else ""
                    ),
                    and_(
                        Buildings.district.like("%" + district_input + "%") if district_input is not None else "",
                        Buildings.num_of_bedrooms.like(
                            "%" + bedrooms_input + "%") if bedrooms_input is not None else "",
                        Buildings.num_of_living_rooms.like(
                            "%" + livingrooms_input + "%") if livingrooms_input is not None else "",
                        Buildings.price_per_meter >= lower_bond if lower_bond is not None else "",
                        Buildings.price_per_meter <= upper_bond if upper_bond is not None else "",
                        Buildings.size >= size_lower_bond if size_lower_bond is not None else "",
                        Buildings.size <= size_upper_bond if size_upper_bond is not None else "",
                        Buildings.building_type.like(
                            "%" + building_type_input + "%") if building_type_input is not None else ""
                        # Buildings.price_per_meter.like("%" + price_per_meter_input + "%") if price_per_meter_input is not None else ""
                    )
                )
                )

                if order is None:
                    u = u.paginate(page=page, per_page=18)

                else:
                    if order == 'Price (Hi-Lo)':
                        u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("1")

                    if order == 'Price (Lo-Hi)':
                        u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("2")

                    if order == 'Lowest SqFt':
                        u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("3")

                    if order == 'Largest SqFt':
                        u = u.order_by(Buildings.price_per_meter.desc()).paginate(page=page, per_page=18)
                        print("4")

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
                if size_input == "":
                    size_input = 'null'
                if building_type_input == "":
                    building_type_input = 'null'

            print("未进行search")
            return render_template('listing.html', u=u.items, pagination=u, search_input=search_input,
                                   district_input=district_input,
                                   bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input,
                                   price_per_meter_input=price_per_meter_input, size_input=size_input,
                                   building_type_input=building_type_input)

    else:
        flash(u'User should login first!','danger')
        return redirect(url_for('login'))

    return render_template('listing.html')

@app.route('/single/<int:id>', methods=['GET', 'POST'])
def single(id=None):
    if not session.get("LOGING_USER") is None:
        form = SingleForm()
        single_property = Buildings.query.filter(Buildings.id == id).first()
        user = User.query.filter(User.id == session.get("LOGING_USER")['userid']).first()
        ratings = Ratings.query.filter(and_(Ratings.house_id == single_property.id, Ratings.user_id == user.id)).first()
        Like = request.form.get('Like')

        # 初次进入页面，设定rating为3
        if not ratings:
            AddLike = Ratings(user_id=user.id, house_id=single_property.id, ratings=3)
            db.session.add(AddLike)
            db.session.commit()
            print("Ratings初始化")

        # 点击喜欢房源按钮
        if Like:
            if ratings:
                if ratings.ratings == 5:
                    ratings.ratings = 3
                else:
                    ratings.ratings = 5

                db.session.commit()
                print("ratings已存在")

            else:
                AddLike = Ratings(user_id=user.id, house_id=single_property.id, ratings=5)
                db.session.add(AddLike)
                db.session.commit()
                print("ratings不存在")

	
	
        filename2 = os.path.dirname(os.path.dirname(__file__)) + r'/blogapp/resources/test2.csv'
        print("load movie embedding")
        mgr_house_embedding = EmbeddingManager(
            filename2, "id", "vector")

        

        if int(single_property.id) > 4000:
            ram = random.randint(0, 9)
            single_property2 = Buildings.query.filter(Buildings.id == ram).first()
        else:
            single_property2 = single_property
        
        # 查询自己的embedding
        house_embedding = mgr_house_embedding.get_embedding(single_property2.id)

        # 查询相似的电影
        house_ids = mgr_house_embedding.search_ids_by_embedding(house_embedding, 7)

        similar_property = []

        for i in house_ids:
            if i == single_property2.id:
                house_ids.remove(single_property2.id)
            else:
                result = Buildings.query.filter(Buildings.id == i).first()
                if result is not None:
                    similar_property.append(result)
        if len(house_ids) == 7:
            house_ids.pop()

        print(similar_property)

        photos_list = {}
        if single_property.photo_2 is not None:
            photos_list['1'] = single_property.photo_2
        if single_property.photo_3 is not None:
            photos_list['2'] = single_property.photo_3
        if form.validate_on_submit():
            if user.first_name is None or user.last_name is None or user.phone is None:
                flash(u"If you want to make an appointment, please let us know your name and phone number first.",'info')
                return redirect(url_for("profile"))
            else:
                user_id = session.get("LOGING_USER")['userid']
                house_id = id
                exist = 0
                message_all = models.Message.query.all();
                exist_message = None
                for m in message_all:
                    if user_id == m.user_id and house_id == m.house_id:
                        exist = 1
                        exist_message = m
                if exist == 0:
                    message = models.Message(user_id=user_id, house_id=house_id, content=form.content.data)
                    db.session.add(message)
                    db.session.commit()
                    flash(u'Message Successfully Sent!','success')
                elif exist == 1:
                    exist_message.content = form.content.data
                    db.session.commit()
                    flash(u'Message Successfully Sent!','success')
                # return redirect('single-property-1.html', single_property=single_property, form=form)
        return render_template('single-property-1.html', single_property=single_property, form=form,
                               photos_list=photos_list, similar_property=similar_property)
    else:
        flash(u'User should login first!', 'danger')
        return redirect(url_for('login'))


@app.route('/message/<int:id>', methods=['GET', 'POST'])
def single_for_message(id=None):
    form1 = EditForm()
    # form2 = DeleteForm()
    if not session.get("LOGING_USER") is None:
        my_property = Buildings.query.filter(Buildings.id == id).first()
        photos_list = {}
        if my_property.photo_2 is not None:
            photos_list['1'] = my_property.photo_2
        if my_property.photo_3 is not None:
            photos_list['2'] = my_property.photo_3
        message_all = models.Message.query.filter(models.Message.house_id == id)
        potential_users = {}
        for message in message_all:
            potential_user = User.query.filter(User.id == message.user_id).first()
            m = message.content
            potential_users[potential_user] = m
        # print(potential_users)
        if form1.submit.data and form1.validate():
            my_property.district = form1.district.data
            my_property.size = form1.size.data
            my_property.building_type = form1.floor_range.data
            my_property.num_of_bedrooms = form1.bedroom_number.data
            my_property.num_of_living_rooms = form1.livingroom_number.data
            my_property.orientation = form1.orientation.data
            my_property.build_time = form1.year.data
            my_property.total_price = form1.total_price.data
            my_property.num_of_floors = form1.floor_number.data
            my_property.price_per_meter = form1.total_price.data * 10000 / form1.size.data
            db.session.commit()
            # print("1")
            return render_template('messages.html', single_property=my_property, potential_users=potential_users,
                                   form1=form1, photos_list=photos_list)

        elif request.method == 'POST':
            # print("2")
            db.session.delete(my_property)
            db.session.commit()
        return render_template('messages.html', single_property=my_property, potential_users=potential_users,
                               form1=form1, photos_list=photos_list)

    else:
        flash(u'User should login first!', 'danger')

    return redirect(url_for('login'))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if not session.get("LOGING_USER") is None:
        form = AddHouseForm()
        photo_filename_1 = "fp1.jpg"
        pre = [0]

        if form.validate_on_submit():
            building = Buildings(district=form.district.data, address=form.address.data,
                                 total_price=form.total_price.data,
                                 price_per_meter=form.total_price.data * 10000 / form.size.data,
                                 build_time=form.year.data,
                                 num_of_bedrooms=form.bedroom_number.data,
                                 num_of_living_rooms=form.livingroom_number.data, size=form.size.data,
                                 orientation=form.orientation.data,
                                 building_type=form.floor_range.data, num_of_floors=form.floor_number.data,
                                 detail=form.detail.data, photo_1=photo_filename_1,
                                 owner_id=session.get('LOGING_USER')["userid"])
            db.session.add(building)
            db.session.commit()

            if form.photo1.data or form.photo2.data or form.photo3.data:
                photo_list = []
                if form.photo1.data is not None:
                    photo_list.append(form.photo1.data)
                if form.photo2.data is not None:
                    photo_list.append(form.photo2.data)
                if form.photo3.data is not None:
                    photo_list.append(form.photo3.data)
                photo_dir = Config.PHOTO_BUILDING_DIR
                x = 1;
                for p in photo_list:
                    if p is not None:
                        photo_obj = p
                        format = photo_obj.filename.rsplit('.', photo_obj.filename.count('.'))[-1]
                        photo_filename = str(building.id) + '_' + str(x) + '.' + format
                        if x == 1:
                            building.photo_1 = photo_filename
                        if x == 2:
                            building.photo_2 = photo_filename
                        if x == 3:
                            building.photo_3 = photo_filename
                        photo_obj.save(os.path.join(photo_dir, photo_filename))
                        x = x + 1

            db.session.commit()

            return render_template('index.html')

        else:
            if request.method == 'POST' and request.values.get("f") is not None:
                dx = int(request.values.get("dx") or 0)
                y = int(request.values.get("y") or 0)
                b = int(request.values.get("b") or 0)
                l = int(request.values.get("l") or 0)
                s = int(request.values.get("s") or 0)
                rx = int(request.values.get("rx") or 0)
                f = int(request.values.get("f") or 0)
                pre = model.predict(
                    [[dx / 15, (y - 1955) / 65, (b - 1) / 8, l / 6, (s - 20) / 616, rx / 5, (f - 1) / 39]])
                print(dx / 15, (y - 1955) / 65, (b - 1) / 8, l / 6, (s - 20) / 616, rx / 5, (f - 1) / 39)
                print(pre[0])
                low = str(0.80*pre[0])
                high = str(1.20*pre[0])

                a, b, c = low.partition('.')
                c = c[:2]
                low1 = ".".join([a, c])

                d, e, f = high.partition('.')
                f = f[:2]
                high1 = ".".join([d, f])

                ss = low1 + " - " + high1
                print(ss)
                nify = {'number': ss}
                return jsonify(nify)

    else:
        flash('User should login first!')
        return redirect(url_for('login'))
    return render_template('post.html', form=form, pre=pre)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginUser = session.get("LOGING_USER")
    form = LoginForm()
    if not session.get("LOGING_USER") is None:
        flash(u'You should log out first!', 'danger')
        return redirect(url_for('profile'))
    else:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.email == form.email.data).first()
            if not user_in_db:
                # flash('No user found with email: {}'.format(form.email.data))
                flash(u'No user found with email: {}'.format(form.email.data), 'danger')
                return redirect(url_for('login'))
            if (check_password_hash(user_in_db.password_hash, form.password.data)):
                session["LOGING_USER"] = {'email': user_in_db.email, 'userid': user_in_db.id}
                return redirect(url_for('index'))
                # return render_template('index.html', user=user_in_db)
            flash(u'Incorrect Password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form, loginUser=loginUser)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    loginUser = session.get("LOGING_USER")
    form = SignupForm()
    if not session.get("LOGING_USER") is None:
        flash(u'You should log out first!', 'danger')
        return redirect(url_for('profile'))
    else:
        if form.validate_on_submit():
            if form.password.data != form.password2.data:
                flash(u'Passwords do not match!', 'danger')
                return redirect(url_for('signup'))
            user_all = User.query.all();
            for u in user_all:
                if form.username.data == u.username:
                    flash(u'User already exist!', 'danger')
                    return redirect(url_for('signup'))
            passw_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash, first_name=None,
                        last_name=None, phone=None, district=None, address=None)
            db.session.add(user)
            db.session.commit()
            flash(u'User registered with username:{}'.format(form.username.data), 'info')
            session["LOGING_USER"] = {'username': user.username, 'userid': user.id}
            return redirect(url_for('profile'))
    return render_template('signup.html', title='Register a new user', form=form, loginUser=loginUser)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if not session.get("LOGING_USER") is None:
        user = User.query.filter(User.id == session.get("LOGING_USER")['userid']).first()
        if not user.photo:
            print('photo is None')
            user.photo = "Admin.jpg"
            db.session.commit()

        if form.validate_on_submit():
            if form.photo.data:
                photo_dir = Config.PHOTO_UPLOAD_DIR
                photo_obj = form.photo.data
                format = photo_obj.filename.rsplit('.', photo_obj.filename.count('.'))[-1]
                photo_filename = user.username + '.' + format
                photo_obj.save(os.path.join(photo_dir, photo_filename))
                user.photo = photo_filename
            else:
                user.photo = user.photo

            if form.phone.data:
                user.phone = form.phone.data
            else:
                user.phone = user.phone

            if form.first_name.data:
                user.first_name = form.first_name.data
            else:
                user.first_name = user.first_name

            if form.last_name.data:
                user.last_name = form.last_name.data
            else:
                user.last_name = user.last_name

            if form.district.data:
                user.district = form.district.data
            else:
                user.district = user.district

            if form.address.data:
                user.address = form.address.data
            else:
                user.address = user.address

            db.session.commit()

        return render_template('profile-new.html', form=form, user=user)
    else:
        flash(u'User should login first!', 'danger')
        return redirect(url_for('login'))


@app.route('/changepassword', methods=['GET', 'POST'])
def change():
    loginUser = session.get('LOGING_USER')
    form = ChangePasswordForm()
    user = User.query.filter(User.id == session.get('LOGING_USER')['userid']).first()
    if form.validate_on_submit():
        if (check_password_hash(user.password_hash, form.old_password.data)):
            if form.new_password.data != form.new_password2.data:
                flash(u'Password do not match!', 'danger')
                return redirect(url_for('change'))
            else:
                passw_hash = generate_password_hash(form.new_password.data)
                user.password_hash = passw_hash
                db.session.commit()
                flash(u'Password Successfully Changed!', 'success')
                return redirect(url_for('profile'))
        else:
            flash(u'Incorrect Password!', 'danger')
            return redirect(url_for('change'))
    return render_template('change-password.html', form=form)


@app.route('/forgot1', methods=['GET', 'POST'])
def forgot():
    form = SendEmailForm()
    global email_for_verify
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.email == form.emailaddress.data).first()
        if not user_in_db:
            flash(u'No user found with email: {}'.format(form.emailaddress.data), 'danger')
        else:
            email_for_verify = user_in_db.email
            source = list(string.ascii_letters)
            source.extend(map(lambda x: str(x), range(0, 10)))
            captcha = "".join(random.sample(source, 6))
            print(captcha)
            global Verification_code
            Verification_code = str(captcha)
            e_body = 'Your veification code is ' + captcha + '. Please use this code to reset your password.'
            message = Message(subject='Verification Code', sender="zhangmengyi1999@126.com",
                              recipients=[email_for_verify], body=e_body)
            time.sleep(5)
            try: 
                mail.send(message)
                return redirect(url_for('reset'))
            except:
                flash(u"server error, unable to send verification message, please try again later", 'danger')

    return render_template('forgot.html', form=form)


@app.route('/forgot2', methods=['GET', 'POST'])
def reset():
    form = VerifyAndResetForm()
    if form.validate_on_submit():
        if form.v_code.data != Verification_code:
            flash(u'Wrong Verification Code!', 'danger')
        else:
            if form.new_password.data != form.new_password2.data:
                flash(u'Passwords do not match', 'danger')
            else:
                user_for_verify = User.query.filter(User.email == email_for_verify).first()
                passw_hash = generate_password_hash(form.new_password.data)
                user_for_verify.password_hash = passw_hash
                db.session.commit()
                flash(u'You have successfully reset your password!', 'success')
                return redirect(url_for('login'))
    return render_template('forgot-reset.html', form=form)


@app.route('/logout')
def logout():
    session.pop("LOGING_USER", None)
    return redirect(url_for('login'))


# @app.route('/message', methods=['GET', 'POST'])
# def message():
#     user_id = session.get("LOGING_USER")['userid']
#     print(user_id)
#     return redirect(url_for('single'))



@app.route('/management/<int:page>', methods=['GET', 'POST'])
def management(page=None):
    if not session.get("LOGING_USER") is None:
        if not page:
            page = 1



        houses = Buildings.query.filter(Buildings.owner_id == session.get("LOGING_USER")['userid'])
        user = User.query.filter(User.id == session.get("LOGING_USER")['userid']).first()

        if request.method == 'POST':
            search_input = request.form.get('content')  # 需要查询的内容
            session['input'] = search_input

            if search_input is None or search_input == "Any" or search_input == "":
                search_input = ""
                session['input'] = search_input

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
                    Buildings.owner_id == user.id
                )
            )
            )

            u = u.paginate(page=page, per_page=18)

            if search_input == "":
                search_input = 'null'


        else:
            if session['input'] == "":
                u = houses.paginate(page=page, per_page=18)

            else:
                search_input = session['input']

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
                        Buildings.owner_id==user.id
                    )
                )
                )

                u = u.paginate(page=page, per_page=18)


        # u = houses.paginate(page=page, per_page=18)
        return render_template('management.html', houses=houses, u=u.items, pagination=u)

    else:
        flash(u'User should login first!', 'danger')
        return redirect(url_for('login'))



print("Calculate user embedding and movie embedding.......")
#pre_embedding = Embedding()
#pre_embedding.pre()

#pre_embedding2 = Embedding2()
#pre_embedding2.pre()


filename1=os.path.dirname(os.path.dirname(__file__))+r'/blogapp/resources/movielens_user_embedding.csv'
print("load user embedding")
mgr_user_embedding = EmbeddingManager(
    # "C:/Users/MSI-PC/Desktop/TEST/blogapp/resources/movielens_user_embedding.csv", "user_id", "house_2vec")
    filename1, "user_id", "house_2vec")

filename2=os.path.dirname(os.path.dirname(__file__))+r'/blogapp/resources/test2.csv'
print("load movie embedding")
mgr_house_embedding = EmbeddingManager(
    filename2, "id", "vector")

filename3=os.path.dirname(os.path.dirname(__file__))+r'/blogapp/resources/ratings.csv'
print("load movie embedding")
obj_user_rating = UserRating(filename3)


filename4=os.path.dirname(os.path.dirname(__file__))+r'/blogapp/resources/buildings.csv'
print("load movie info")
obj_house_info = HouseInfo(filename4)


if __name__ == '__main__':
    app.run()
