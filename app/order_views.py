import datetime

from flask import Blueprint, render_template, request, session, jsonify

from app.models import House, Order

order_blue = Blueprint('order', __name__)


# 我的订单
@order_blue.route('/order/', methods=['GET'])
def orders():
    return render_template('orders.html')


# 客户订单
@order_blue.route('/lorder/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 创建订单
@order_blue.route('/create_order/', methods=['POST'])
def create_order():
    id=request.form.get('id')
    sd=request.form.get('sd')
    ed=request.form.get('ed')
    user_id = session.get('user_id')
    sd = datetime.datetime.strptime(sd, '%Y-%m-%d')
    ed = datetime.datetime.strptime(ed, '%Y-%m-%d')
    days = (ed - sd).days
    house = House.query.filter(House.id == id).first()
    price = house.price
    amount = days*price
    order = Order()
    order.user_id = user_id
    order.house_id = id
    order.begin_date = sd
    order.end_date = ed
    order.days = days
    order.house_price = price
    order.amount = amount
    order.status = 'WAIT_ACCEPT'
    order.add_update()
    return jsonify({'code':200})


# 获取我的订单
@order_blue.route('/get_my_order/', methods=['GET'])
def get_my_order():
    user_id = session.get('user_id')
    orders = Order.query.filter(Order.user_id == user_id).all()
    order_dict = [order.to_dict() for order in orders]
    data = {'code': 200, 'order': order_dict}
    return jsonify(data)
