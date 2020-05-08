from flask import render_template, request, make_response, redirect
from mysite import classes, dao, app
from mysql.connector import Error
from mysite import util
import random
import string


def make_nav_panel(index_bold):
    nav = classes.Navigation(index_bold)
    home = classes.NavItem( "Домашняя страница", "/")
    product_list = classes.NavItem( "Список товаров сайта", "/productlist/")
    sertification = classes.NavItem( "Сертификаты продукции", "/certificates/")
    about_us = classes.NavItem( "О нас", "/aboutus/")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)
    return nav


#  Func, that idintificate User via token from cookies.
def user_identification():
    token = request.cookies.get('token')
    if token != None:
        cursor = dao.cnx.cursor()
        cursor.execute("SELECT id, login FROM user WHERE token = %s", (token, )) 
        result = cursor.fetchone()
        cursor.close()
        user = classes.User(result[0], result[1])
        return user
    return None


def user_log(user_identification):
    user = user_identification()
    if user != None:
        u_login = user.login 
    else:
        u_login = None
    return u_login


@app.route('/')
def index():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, link, image FROM category")
    result = cursor.fetchall()
    cursor.close()
 
    products = []
    for row in result:
        products.append(classes.Product.from_db_row(row))
 
    nav = make_nav_panel(0)

    u_login = user_log(user_identification)    
   
    return render_template('index.html', products=products, nav=nav, u_login=u_login)


@app.route('/productlist/')
def productlist():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product")
    result = cursor.fetchall()
    cursor.close()
   
    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel(1)

    u_login = user_log(user_identification)

    return render_template('productlist.html', items=items, nav=nav, u_login=u_login)

@app.route('/certificates/')
def certificates():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, image FROM certificate")
    result = cursor.fetchall()
    cursor.close()
       
    items = []
    for row in result:
        items.append(classes.Certificate.from_db_row(row))

    nav = make_nav_panel(2)

    u_login = user_log(user_identification)

    text = "В подтвержение качества и подлинности нашей продукции для Вас мы разместили сертифкаты и свидетельства о госрегистрации."

    return render_template("certificates.html", items=items, nav=nav, text=text, u_login=u_login)

@app.route('/registration/')
def registration():

    nav = make_nav_panel(3)

    u_login = user_log(user_identification)

    return render_template("registration.html", nav=nav, u_login=u_login)

@app.route('/send_form', methods=['GET', 'POST'])
def send_form():

    nav = make_nav_panel(3)

    u_login = user_log(user_identification)
    
    if request.method == 'POST':
        try:
            cursor = dao.cnx.cursor(buffered=True)
            query_login = "SELECT 1 FROM user WHERE login = %s"
            query_email = "SELECT 1 FROM user WHERE email = %s"        
            sql = "INSERT INTO user (login, name, surname, email, mobilenumber, dob, town, password, token) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_login, (request.form['user_login'],))
            res1 = cursor.fetchone()
            cursor.execute(query_email, (request.form['user_email'],))
            res2 = cursor.fetchone()
            if res1 == None and res2 == None:
                user_pass_hash = util.do_password_hash(request.form['user_pass'])
                token = util.random_string()
                user_info = (
                request.form['user_login'], request.form['user_name'], request.form['user_surname'], 
                request.form['user_email'], request.form['user_mobilenumber'], request.form['user_dob'], 
                request.form['user_town'], user_pass_hash, token, 
                )
                cursor.execute(sql, user_info)                
                dao.cnx.commit()
                resp = make_response(redirect('/'))
                resp.set_cookie('token', '%s' % token, max_age=43200)
            elif res1 != None and res2 != None:
                error = "Этот логин и e-mail уже заняты!"
                dao.cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)
            elif res1 != None:
                error = "Этот логин уже занят!"
                dao.cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)
            else:
                error = "Этот e-mail уже занят!"
                dao.cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)               
        except:
            error = "Ошибка при регистрации аккаунта! Попробуйте еще раз!"
            dao.cnx.rollback()
            return render_template('registration.html', error=error,nav=nav)
        cursor.close()
    return resp


@app.route('/aboutus/')
def aboutus():

    nav = make_nav_panel(4)

    u_login = user_log(user_identification)

    return render_template("aboutus.html", nav=nav, u_login=u_login)

@app.route('/proteins/')
def proteins():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=1")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас вы можете заказать протеины ведущих фирм премиум-качества.'

    return render_template('proteins.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/gainers/')
def gainers():   
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=2")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас вы можете заказать гейнеры ведущих фирм премиум-качества.'

    return render_template('gainers.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/aminoacids/')
def aminoacids():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=3")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные аминокислоты ведущих фирм премиум-качества.'

    return render_template('aminoacids.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/creatine/')
def creatine():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=4")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас Вы можете креатин ведущих фирм премиум-качества.'

    return render_template('creatine.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/burnfats/')
def burnfats():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=5")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас Вы можете заказать жиросжигатели ведущих фирм премиум-качества.'

    return render_template('burnfats.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/vitamins/')
def vitamins():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=6")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные витамины ведущих фирм премиум-качества.'

    return render_template('vitamins.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/steroids/')
def steroids():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=7")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    text = "У нас Вы можете заказать как комплексные, так и отдельные 'витамины' ведущих фирм премиум-качества."

    return render_template('steroids.html', nav=nav, items=items, text=text, u_login=u_login)

@app.route('/login/', methods=["GET", "POST"])
def login():
    nav = make_nav_panel("None")

    u_login = user_log(user_identification)

    if request.method == "POST":
        cursor = dao.cnx.cursor(buffered=True)
        query_login_password = "SELECT password FROM user WHERE login = %s"
        cursor.execute(query_login_password, (request.form["login_field"], ))
        res = cursor.fetchone()
        if res != None:
            verify_valid = util.password_verify(res[0], request.form["password_field"])
            if verify_valid == True:
                token = util.random_string()
                set_token = "UPDATE user SET token = %s WHERE login = %s"
                cursor.execute(set_token, (token, request.form["login_field"], ))
                dao.cnx.commit()
                cursor.close()
                resp = make_response(redirect('/'))
                resp.set_cookie('token', '%s' % token, max_age=43200) 
                return resp
        else:
            error = "*Данная комбинация логина/пароля введена с ошибкой либо не существует!"
            return render_template("login.html", nav=nav, error=error)            
    return render_template("login.html", nav=nav, u_login=u_login)


@app.route('/logout/')
def logout():
    user = user_identification()
    cursor = dao.cnx.cursor()
    cursor.execute('UPDATE user SET token = NULL WHERE id = %s', (user.user_id, ))
    dao.cnx.commit()
    cursor.close()

    resp = make_response(redirect('/'))
    resp.delete_cookie('token')

    return resp


