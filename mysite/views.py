from flask import render_template, request, make_response, redirect, jsonify
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
        res = cursor.fetchone()
        user = classes.User(res[0], res[1])

        query = 'SELECT product_id, count FROM shopping_cart WHERE user_id = %s'
        cursor.execute(query, (user.user_id, ))
        result = cursor.fetchall()
        if result != None:
            for i in range(len(result)):
                user.push(result[i][0], result[i][1])
        cursor.close()
        return user
    return 'User undefined!'


@app.route('/')
def index():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, link, image FROM category")
    result = cursor.fetchall()
    cursor.close()
 
    categories = []
    for row in result:
        categories.append(classes.Category.from_db_row(row))
 
    nav = make_nav_panel(0)
    user = user_identification()
    #u_login = user_log(user_identification)    
   
    return render_template('index.html', categories=categories, nav=nav, user=user)


@app.route('/productlist/')
def productlist():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product")
    result = cursor.fetchall()
    cursor.close()
   
    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel(1)

    user = user_identification()

    text = 'На данной странице вы можете ознакомиться со всеми представленными на сайте товарами.'

    return render_template('productlist.html', items=items, nav=nav, user=user, text=text)


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

    user = user_identification()

    text = "В подтвержение качества и подлинности нашей продукции для Вас мы разместили сертифкаты и свидетельства о госрегистрации."

    return render_template("certificates.html", items=items, nav=nav, text=text, user=user)


@app.route('/registration/')
def registration():

    nav = make_nav_panel(3)

    user = user_identification()

    return render_template("registration.html", nav=nav, user=user)


@app.route('/send_form', methods=['GET', 'POST'])
def send_form():  
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

    user = user_identification()

    return render_template("aboutus.html", nav=nav, user=user)


@app.route('/proteins/')
def proteins():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=1")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")
    user = user_identification()

    text = 'У нас вы можете заказать протеины ведущих фирм премиум-качества.'

    return render_template('proteins.html', nav=nav, items=items, text=text, user=user)


@app.route('/gainers/')
def gainers():   
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=2")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = 'У нас вы можете заказать гейнеры ведущих фирм премиум-качества.'

    return render_template('gainers.html', nav=nav, items=items, text=text, user=user)


@app.route('/aminoacids/')
def aminoacids():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=3")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = 'У нас Вы можете заказать как комплексные, так и отдельные аминокислоты ведущих фирм премиум-качества.'

    return render_template('aminoacids.html', nav=nav, items=items, text=text, user=user)


@app.route('/creatine/')
def creatine():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=4")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = 'У нас Вы можете креатин ведущих фирм премиум-качества.'

    return render_template('creatine.html', nav=nav, items=items, text=text, user=user)


@app.route('/burnfats/')
def burnfats():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=5")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = 'У нас Вы можете заказать жиросжигатели ведущих фирм премиум-качества.'

    return render_template('burnfats.html', nav=nav, items=items, text=text, user=user)


@app.route('/vitamins/')
def vitamins():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=6")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = 'У нас Вы можете заказать как комплексные, так и отдельные витамины ведущих фирм премиум-качества.'

    return render_template('vitamins.html', nav=nav, items=items, text=text, user=user)


@app.route('/steroids/')
def steroids():
    cursor = dao.cnx.cursor()
    cursor.execute("SELECT id, name, about, image FROM product WHERE  category_id=7")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    user = user_identification()

    text = "У нас Вы можете заказать как комплексные, так и отдельные 'витамины' ведущих фирм премиум-качества."

    return render_template('steroids.html', nav=nav, items=items, text=text, user=user)


@app.route('/login/', methods=["GET", "POST"])
def login():
    nav = make_nav_panel("None")

    user = user_identification()

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
    return render_template("login.html", nav=nav, user=user)


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


# Endpoint, that append items to user's shopping cart.
@app.route('/add_to_cart', methods = ['POST'])
def add_to_cart():
    user_data = request.get_json()
    user_id = user_data['user_id']
    product_id = user_data['product_id']
    count = user_data['count']

    query = '''INSERT INTO shopping_cart (product_id, user_id, count) VALUES (%s, %s, %s) 
    ON DUPLICATE KEY UPDATE count=count + %s'''
    cursor = dao.cnx.cursor()
    cursor.execute(query, (product_id, user_id, count, count, ))
    dao.cnx.commit()

    user = user_identification()

    return jsonify({ 'users_shopping_cart' : user.shopping_cart })


# Rendering shopping cart page.
@app.route('/shopping_cart/')
def shopping_cart():
    nav = make_nav_panel('None')

    user = user_identification()

    cursor = dao.cnx.cursor()
    items = []
    query = "SELECT id, name, about, image FROM product WHERE id=%s"
    for position in user.shopping_cart:
        cursor.execute(query, (position, ))
        result = cursor.fetchone()
        items.append(classes.Product.from_db_row(result))
    cursor.close()
        
    return render_template("shopping_cart.html", nav=nav, user=user, items=items)


#  Method, that delete position from the user's shopping cart.
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    user_data = request.get_json()
    user_id = user_data['user_id']
    product_id = user_data['product_id']

    query = "DELETE FROM shopping_cart WHERE user_id = %s AND product_id = %s"
    cursor = dao.cnx.cursor()
    cursor.execute(query, (user_id, product_id, ))
    dao.cnx.commit()
    cursor.close()

    user = user_identification()

    return jsonify({'user_cart' : user.shopping_cart })






