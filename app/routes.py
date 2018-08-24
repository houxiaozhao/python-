from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title="主页", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 先判断是否已经登陆
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 得到表单数据
    form = LoginForm()
    print(form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # 查询数据库
        if user is None or not user.check_password(form.password.data):  # 有该用户并且密码正确
            flash('错误的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # 如果登录URL中不含next参数，那么将会重定向到本应用的主页。
        # 如果登录URL中包含next参数，其值是一个相对路径（换句话说，该URL不含域名信息），那么将会重定向到本应用的这个相对路径。
        # 如果登录URL中包含next参数，其值是一个包含域名的完整URL，那么重定向到本应用的主页。
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="sign in", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
