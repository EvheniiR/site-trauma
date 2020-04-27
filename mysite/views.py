from flask import render_template, request, make_response, redirect
from mysite import classes, dao, app
from mysql.connector import Error
import random
import string


def make_nav_panel(index_bold):
    nav = classes.Navigation(index_bold)
    home = classes.NavItem( "Домашняя страница", "/")
    product_list = classes.NavItem( "Список товаров сайта", "/productlist/")
    sertification = classes.NavItem( "Сертификаты продукции", "/certificates/")
    registration = classes.NavItem("Регистрация", "/registration/")
    about_us = classes.NavItem( "О нас", "/aboutus/")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)
    return nav


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
   
    return render_template('index.html', products=products, nav=nav)


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

    return render_template('productlist.html', items=items, nav=nav)

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

    text = "В подтвержение качества и подлинности нашей продукции для Вас мы разместили сертифкаты и свидетельства о госрегистрации."

    return render_template("certificates.html", items=items, nav=nav, text=text)

@app.route('/registration/')
def registration():

    nav = make_nav_panel(3)

    return render_template("registration.html", nav=nav)

@app.route('/send_form', methods=['GET', 'POST'])
def send_form():

    nav = make_nav_panel(3)
    
    if request.method == 'POST':
        user_info = (request.form['user_login'], request.form['user_name'], request.form['user_surname'], request.form['user_email'], request.form['user_mobilenumber'], request.form['user_dob'], request.form['user_town'], request.form['user_pass'],)
        try:
            cursor = dao.cnx.cursor(buffered=True)
            query_login = "SELECT 1 FROM user WHERE login = %s"
            query_email = "SELECT 1 FROM user WHERE email = %s"        
            sql = "INSERT INTO user (login, name, surname, email, mobilenumber, dob, town, password) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_login, (request.form['user_login'],))
            res1 = cursor.fetchone()
            cursor.execute(query_email, (request.form['user_email'],))
            res2 = cursor.fetchone()
            if res1 == None and res2 == None:
                cursor.execute(sql, user_info)
                dao.cnx.commit()
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
        except mysql.connector.Error as err:
            error = "Ошибка при регистрации аккаунта! Попробуйте еще раз!"
            dao.cnx.rollback()

            return render_template('registration.html', error=error,nav=nav)

        finally:
            cursor.close()

    return render_template('registration_done.html', name=request.form['user_name'], nav=nav)


@app.route('/aboutus/')
def aboutus():

    nav = make_nav_panel(4)

    return render_template("aboutus.html", nav=nav)

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

    text = 'У нас вы можете заказать протеины ведущих фирм премиум-качества.'
    return render_template('proteins.html', nav=nav, items=items, text=text)

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

    text = 'У нас вы можете заказать гейнеры ведущих фирм премиум-качества.'

    return render_template('gainers.html', nav=nav, items=items, text=text)

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

    text = 'У нас Вы можете заказать как комплексные, так и отдельные аминокислоты ведущих фирм премиум-качества.'

    return render_template('aminoacids.html', nav=nav, items=items, text=text)

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

    text = 'У нас Вы можете креатин ведущих фирм премиум-качества.'

    return render_template('creatine.html', nav=nav, items=items, text=text)

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

    text = 'У нас Вы можете заказать жиросжигатели ведущих фирм премиум-качества.'

    return render_template('burnfats.html', nav=nav, items=items, text=text)

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

    text = 'У нас Вы можете заказать как комплексные, так и отдельные витамины ведущих фирм премиум-качества.'

    return render_template('vitamins.html', nav=nav, items=items, text=text)

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

    text = "У нас Вы можете заказать как комплексные, так и отдельные 'витамины' ведущих фирм премиум-качества."

    return render_template('steroids.html', nav=nav, items=items, text=text)

@app.route('/login/', methods=["GET", "POST"])
def login():

    cursor = dao.cnx.cursor()
    cursor.execute("SELECT name, link, image FROM category")
    result = cursor.fetchall()
    cursor.close()
    products = []
    for row in result:
        products.append(classes.Product.from_db_row(row))

    nav = make_nav_panel("None")

    if request.method == "POST":
        cursor = dao.cnx.cursor(buffered=True)
        query_login_password = "SELECT id FROM user WHERE login = %s AND password = %s"
        cursor.execute(query_login_password, (request.form["login_field"], request.form["password_field"], ))
        res = cursor.fetchone()
        if res != None:
            def random_string(stringLength=30):
                letters = string.ascii_lowercase 
                return ''.join(random.choice(letters) for i in range(stringLength))
            token = random_string()
            set_token = "UPDATE user SET token = %s WHERE id = %s"
            cursor.execute(set_token, (token, res[0], ))
            dao.cnx.commit()

            resp = make_response(redirect('/'))
            resp.set_cookie('login', '%s' % request.form["login_field"])
            resp.set_cookie('token', '%s' % token)
            return resp
        else:
            error = "*Данная комбинация логина/пароля введена с ошибкой либо не существует!"
            return render_template("login.html", nav=nav, error=error)            
        cursor.close()

    return render_template("login.html", nav=nav)
