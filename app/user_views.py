import os
import random
import re

from flask import Blueprint, render_template, jsonify, session, request

from app.models import User
from utils.functions import is_login
from utils.setting import MEDIA_PATH

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 注册
@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')

    # 1,验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 2001, 'msg': '请填写完整'})

    # 2，验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 2002, 'msg': '手机号不对'})

    # 3，验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 2003, 'msg': '验证码不对'})

    # 4，密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 2004, 'msg': '密码不一致'})

    # 验证手机号是否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 2005, 'msg': '手机号被注册了'})

    # 创建注册信息 (保存）
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


# 获取验证码
@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片地址
    # 方式2：后端值生成随机参数，返回给页面，在页面中生成图片
    s = '1234567890qwertuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


# 登录
@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/login/', methods=['POST'])
def my_login():
    # 实现登录
    phone = request.form.get('phone')
    pwd = request.form.get('pwd')
    # 参数是否填写完成
    if not all([phone, pwd]):
        return jsonify({'code': 2006, 'msg': '填写完整'})
    # 获取手机对应得用户信息
    user = User.query.filter(User.phone == phone).first()
    if not user:
        return jsonify({'code': 2007, 'msg': '没注册'})
    # 效验密码是否正确
    if not user.check_pwd(pwd):
        return jsonify({'code': 2008, 'msg': '密码不对'})
    # 登录标识设置
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '请求成功'})


# 我的
@user_blue.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 个人中心
@user_blue.route('/user_info/', methods=['GET'])
def user_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code': 200, 'msg': '成功', 'data': user.to_basic_dict()})


# 首页
@user_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@user_blue.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


# 上传用户名
@user_blue.route('/user_name/', methods=['PATCH'])
def up_name():
    user_name = request.form.get('user_name')
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.name = user_name
    user.add_update()
    return jsonify({'code': 200, 'msg': '用户名修改成功'})


# 上传头像
@user_blue.route('/user_avatar/', methods=['PATCH'])
def up_avatar():
    img = request.files.get('avatar')
    path = os.path.join(MEDIA_PATH, img.filename)
    img.save(path)
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.avatar = img.filename
    user.add_update()
    return jsonify({'code': 200,  'msg': '头像上传成功', 'avatar': img.filename})


# 实名认证
@user_blue.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


# 实名认证
@user_blue.route('/auth/', methods=['POST'])
def my_auth():
    id_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    if not all(['real_name', 'id_card']):
        return jsonify({'code': 3001, 'msg': '请输入完整信息'})
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.id_name = id_name
    user.id_card = id_card
    user.add_update()
    return jsonify({'code': 200, 'msg': '实名认证成功'})


# 登录后首页
@user_blue.route('/user_info1/', methods=['GET'])
def user_info1():
    # 拿到session中的当前登录用户的id
    user_id = session.get('user_id')
    # 通过用户的id去数据库中拿到用户信息
    user = User.query.get(user_id)
    # 从数据库中拿到用户的名字（用户名）
    username = user.name
    # 成功后返回200状态码，并将数据返回给前端
    return jsonify({'code': 200, 'msg': '已登录', 'user': user_id, 'username': username})
