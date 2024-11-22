from flask import render_template, request, redirect
import dao
from app import app, login
import math
from flask_login import login_user, logout_user, login_required
import hashlib


@app.route("/")
def index():
    cates = dao.load_categories()

    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page')
    prods = dao.load_products(cate_id=cate_id, kw=kw, page=page)
    return render_template('index.html', categories=cates, products=prods, total_page=math.ceil(dao.count_products()/app.config['PAGE_SIZE']))



@app.route("/login", methods=['GET', 'POST'])
def login_process():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect("/")

    return render_template('login.html')

@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/logout")
@login_required
def logout_process():
    logout_user()
    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register_process():
    if request.method == 'POST':
        data = request.form.copy()
        del data['confirm_password']
        dao.create_user(data)
        print(data)
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
