import math

from flask import render_template, request, redirect, session, jsonify
import dao, utils
from app import app, login
from flask_login import login_user, logout_user
from app.models import UserRole

@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1)
    prods = dao.load_products(cate_id = cate_id, page = (int)(page))
    page_size = app.config.get('PAGE_SIZE',8)
    total = dao.count_products()


    return render_template('index.html', categories = cates, products = prods, page = math.ceil(total/page_size))

@app.route("/login", methods=['get', 'post'])
def login_procee():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect('/')



    return render_template('login.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/logout")
def logout_procees():
    logout_user()
    return redirect('/login')

@app.route("/login-admin", methods=['POST'])
def login_admin_procees():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password, role=UserRole.ADMIN)
        if u:
            login_user(u)
            return redirect('/admin')
        return redirect('/admin')

@app.route("/api/carts", methods=['POST'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart={}

    id = request.json.get("id")
    name = request.json.get("name")
    price = request.json.get("price")

    if id in cart:
        cart[id]["quantity"] +=1
    else:
        cart[id]={
            "id": id,
            "name": name,
            "price": 123,
            "quantity": 1
        }
    session['cart'] = cart
    print(cart)
    return jsonify(utils.stats_cart(cart))

if __name__ == '__main__':

    from app import admin
    app.run(debug=True)
