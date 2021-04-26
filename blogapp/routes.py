import base64
import os

from sqlalchemy import or_, and_
from werkzeug.security import check_password_hash, generate_password_hash
from blogapp import app, db, models, mail
from flask import Flask, render_template, request, session, redirect, url_for, flash
from blogapp.config import Config
from blogapp.models import Buildings, User, Message
from blogapp.forms import search_buildings, search_conditions, LoginForm, SignupForm, ProfileForm, \
    ChangePasswordForm, AddHouseForm, SendEmailForm, VerifyAndResetForm, SingleForm
from flask_mail import Message
import random
import string

# app = Flask(__name__)
# app.config.from_object(Config)
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # root用户名123456密码 test数据库
# db.__init__(app)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': ' '}
    session['name'] = ""
    session['district'] = ""
    session['bedrooms'] = ""
    session['livingrooms'] = ""
    session['price_per_meter'] = ""
    return render_template('index.html', title='Home', user=user)


@app.route(
    '/listing/<int:page><string:name><string:district><string:bedrooms><string:livingrooms><string:price_per_meter>',
    methods=['post', 'get'])
def listing(page=None, name=None, district=None, bedrooms=None, livingrooms=None, price_per_meter=None):
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
                    Buildings.num_of_living_rooms.like(
                        "%" + livingrooms_input + "%") if livingrooms_input is not None else "",
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
                                   bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input,
                                   price_per_meter_input=price_per_meter_input)

        else:
            print("成功2")
            if session['name'] == "" and session['district'] == "" and session['bedrooms'] == "" and session[
                'livingrooms'] and session['price_per_meter'] == "":
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
                                   bedrooms_input=bedrooms_input, livingrooms_input=livingrooms_input,
                                   price_per_meter_input=price_per_meter_input)

    else:
        flash('User should login first!')
        return redirect(url_for('login'))

    return render_template('listing.html')


@app.route('/single/<int:id>', methods=['GET', 'POST'])
def single(id=None):
    if not session.get("LOGING_USER") is None:
        form = SingleForm()
        single_property = Buildings.query.filter(Buildings.id == id).first()
        if form.validate_on_submit():
            user_id = session.get("LOGING_USER")['userid']
            house_id = id
            exist=0
            message_all = models.Message.query.all();
            for m in message_all:
                if user_id==m.user_id and house_id==m.house_id:
                    exist=1
            if exist==0:
                message = models.Message(user_id=user_id, house_id=house_id, content=form.content.data)
                db.session.add(message)
                db.session.commit()
            # return redirect('single-property-1.html', single_property=single_property, form=form)
        return render_template('single-property-1.html', single_property=single_property, form=form)
    else:
        flash('User should login first!')
        return redirect(url_for('login'))

@app.route('/message/<int:id>', methods=['GET', 'POST'])
def single_for_message(id=None):
    if not session.get("LOGING_USER") is None:
        single_property = Buildings.query.filter(Buildings.id == id).first()
        message_all=models.Message.query.filter(models.Message.house_id == id)
        potential_users={}
        for message in message_all:
            potential_user=User.query.filter(User.id==message.user_id).first()
            m=message.content
            potential_users[potential_user]=m
        # print(potential_users)
        return render_template('messages.html', single_property=single_property, potential_users=potential_users)

    else:
        flash('User should login first!')
        return redirect(url_for('login'))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if not session.get("LOGING_USER") is None:
        form = AddHouseForm()
        photo_filename = "fp1.jpg"
        if form.validate_on_submit():
            if form.photo.data:
                photo_dir = Config.PHOTO_BUILDING_DIR
                photo_obj = form.photo.data
                format = photo_obj.filename.rsplit('.', photo_obj.filename.count('.'))[-1]
                photo_filename = form.address.data + '.' + format
                photo_obj.save(os.path.join(photo_dir, photo_filename))
            else:
                photo_filename = photo_filename
            building = Buildings(district=form.district.data, address=form.address.data,
                                 total_price=form.total_price.data,
                                 price_per_meter=form.total_price.data * 10000 / form.size.data,
                                 build_time=form.year.data,
                                 num_of_bedrooms=form.bedroom_number.data,
                                 num_of_living_rooms=form.livingroom_number.data, size=form.size.data,
                                 orientation=form.orientation.data,
                                 building_type=form.floor_range.data, num_of_floors=form.floor_number.data,
                                 detail=form.detail.data, photo=photo_filename, owner_id=session.get('LOGING_USER')["userid"])

            db.session.add(building)
            db.session.commit()
            return render_template('index.html')
    else:
        flash('User should login first!')
        return redirect(url_for('login'))

    return render_template('post.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginUser = session.get("LOGING_USER")
    form = LoginForm()
    if not session.get("LOGING_USER") is None:
        flash('You should log out first!')
        return redirect(url_for('profile'))
    else:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.email == form.email.data).first()
            if not user_in_db:
                flash('No user found with email: {}'.format(form.email.data))
                return redirect(url_for('login'))
            if (check_password_hash(user_in_db.password_hash, form.password.data)):
                session["LOGING_USER"] = {'email': user_in_db.email, 'userid': user_in_db.id}
                return render_template('index.html', user=user_in_db)
            flash('Incorrect Password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form, loginUser=loginUser)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    loginUser = session.get("LOGING_USER")
    form = SignupForm()
    if not session.get("LOGING_USER") is None:
        flash('You should log out first!')
        return redirect(url_for('profile'))
    else:
        if form.validate_on_submit():
            if form.password.data != form.password2.data:
                flash('Passwords do not match!')
                return redirect(url_for('signup'))
            user_all = User.query.all();
            for u in user_all:
                if form.username.data == u.username:
                    flash('User already exist!')
                    return redirect(url_for('signup'))
            passw_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash, first_name=None,
                        last_name=None, phone=None, district=None, address=None)
            db.session.add(user)
            db.session.commit()
            flash('User registered with username:{}'.format(form.username.data))
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
        flash('User should login first!')
        return redirect(url_for('login'))


@app.route('/changepassword', methods=['GET', 'POST'])
def change():
    loginUser = session.get('LOGING_USER')
    form = ChangePasswordForm()
    user = User.query.filter(User.id == session.get('LOGING_USER')['userid']).first()
    if form.validate_on_submit():
        if (check_password_hash(user.password_hash, form.old_password.data)):
            if form.new_password.data != form.new_password2.data:
                flash('Password do not match!')
                return redirect(url_for('change'))
            else:
                passw_hash = generate_password_hash(form.new_password.data)
                user.password_hash = passw_hash
                db.session.commit()
                flash('Password Successfully Changed!')
                return redirect(url_for('profile'))
        else:
            flash('Incorrect Password!')
            return redirect(url_for('change'))
    return render_template('change-password.html', form=form)


@app.route('/forgot1', methods=['GET', 'POST'])
def forgot():
    form = SendEmailForm()
    global email_for_verify
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.email == form.emailaddress.data).first()
        if not user_in_db:
            flash('No user found with email: {}'.format(form.emailaddress.data))
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
            try:
                mail.send(message)
                return redirect(url_for('reset'))
            except:
                flash("server error, unable to send verification message, please try again later")

    return render_template('forgot.html', form=form)


@app.route('/forgot2', methods=['GET', 'POST'])
def reset():
    form = VerifyAndResetForm()
    if form.validate_on_submit():
        if form.v_code.data != Verification_code:
            flash('Wrong Verification Code!')
        else:
            if form.new_password.data != form.new_password2.data:
                flash('Passwords do not match')
            else:
                user_for_verify = User.query.filter(User.email == email_for_verify).first()
                passw_hash = generate_password_hash(form.new_password.data)
                user_for_verify.password_hash = passw_hash
                db.session.commit()
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
        # user=User.query.filter(User.id==session.get("LOGING_USER")['userid']).first()
        houses = Buildings.query.filter(Buildings.owner_id == session.get("LOGING_USER")['userid'])
        # houses = []
        # for i in management:
        #     house = Buildings.query.filter(i.house_id == Buildings.id).first()
        #     houses.append(house)
        u = houses.paginate(page=page, per_page=18)
        return render_template('management.html', houses=houses, u=u.items, pagination=u)

    else:
        flash('User should login first!')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
