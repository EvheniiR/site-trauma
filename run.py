from flask import Flask, render_template, request, make_response, redirect
from classes import*
import mysql.connector
from mysql.connector import Error
import random
import string
import os

app = Flask(__name__)

TRAUMA_DB_LOGIN = os.getenv('TRAUMA_DB_LOGIN')
TRAUMA_DB_PASSWORD = os.getenv('TRAUMA_DB_PASSWORD')
if TRAUMA_DB_LOGIN == None:
    print('Set database login into Environment Variables!')
    exit(1)
elif TRAUMA_DB_PASSWORD == None:
    print('Set database password into Environment Variables!')
    exit(1)
else:
    cnx = mysql.connector.connect(user=TRAUMA_DB_LOGIN, password=TRAUMA_DB_PASSWORD, host='127.0.0.1', database='shop_db')

cnx.autocommit = False

@app.route('/')
def index():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, link, image FROM category")
    result = cursor.fetchall()
    cursor.close()
 
    products = []
    for row in result:
        products.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(0)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)
    return render_template('index.html', products=products, nav=nav)

@app.route('/productlist/')
def productlist():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product")
    result = cursor.fetchall()
    cursor.close()
   
    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(1)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)
    return render_template('productlist.html', items=items, nav=nav)

@app.route('/certificates/')
def certificates():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, image FROM certificate")
    result = cursor.fetchall()
    cursor.close()
       
    items = []
    for row in result:
        items.append(Certificate.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(2)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = "В подтвержение качества и подлинности нашей продукции для Вас мы разместили сертифкаты и свидетельства о госрегистрации."

    return render_template("certificates.html", items=items, nav=nav, text=text)

@app.route('/registration/')
def registration():

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(3)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    return render_template("registration.html", nav=nav)

@app.route('/send_form', methods=['GET', 'POST'])
def send_form():

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(3)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)
    
    if request.method == 'POST':
        user_info = (request.form['user_login'], request.form['user_name'], request.form['user_surname'], request.form['user_email'], request.form['user_mobilenumber'], request.form['user_dob'], request.form['user_town'], request.form['user_pass'],)
        try:
            cursor = cnx.cursor(buffered=True)
            query_login = "SELECT 1 FROM user WHERE login = %s"
            query_email = "SELECT 1 FROM user WHERE email = %s"        
            sql = "INSERT INTO user (login, name, surname, email, mobilenumber, dob, town, password) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_login, (request.form['user_login'],))
            res1 = cursor.fetchone()
            cursor.execute(query_email, (request.form['user_email'],))
            res2 = cursor.fetchone()
            if res1 == None and res2 == None:
                cursor.execute(sql, user_info)
                cnx.commit()
            elif res1 != None and res2 != None:
                error = "Этот логин и e-mail уже заняты!"
                cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)
            elif res1 != None:
                error = "Этот логин уже занят!"
                cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)
            else:
                error = "Этот e-mail уже занят!"
                cnx.rollback()
                return render_template('registration.html', error=error,nav=nav)
                
        except mysql.connector.Error as err:
            error = "Ошибка при регистрации аккаунта! Попробуйте еще раз!"
            cnx.rollback()

            return render_template('registration.html', error=error,nav=nav)

        finally:
            cursor.close()

    return render_template('registration_done.html', name=request.form['user_name'], nav=nav)


@app.route('/aboutus/')
def aboutus():

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(4)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    return render_template("aboutus.html", nav=nav)

@app.route('/proteins/')
def proteins():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=1")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)
    text = 'У нас вы можете заказать протеины ведущих фирм премиум-качества.'
    return render_template('proteins.html', nav=nav, items=items, text=text)

@app.route('/gainers/')
def gainers():   
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=2")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")
    
    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = 'У нас вы можете заказать гейнеры ведущих фирм премиум-качества.'

    return render_template('gainers.html', nav=nav, items=items, text=text)

@app.route('/aminoacids/')
def aminoacids():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=3")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные аминокислоты ведущих фирм премиум-качества.'

    return render_template('aminoacids.html', nav=nav, items=items, text=text)

@app.route('/creatine/')
def creatine():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=4")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = 'У нас Вы можете креатин ведущих фирм премиум-качества.'

    return render_template('creatine.html', nav=nav, items=items, text=text)

@app.route('/burnfats/')
def burnfats():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=5")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = 'У нас Вы можете заказать жиросжигатели ведущих фирм премиум-качества.'

    return render_template('burnfats.html', nav=nav, items=items, text=text)

@app.route('/vitamins/')
def vitamins():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=6")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные витамины ведущих фирм премиум-качества.'

    return render_template('vitamins.html', nav=nav, items=items, text=text)

@app.route('/steroids/')
def steroids():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product WHERE  category_id=7")
    result = cursor.fetchall()
    cursor.close()

    items = []
    for row in result:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    text = "У нас Вы можете заказать как комплексные, так и отдельные 'витамины' ведущих фирм премиум-качества."

    return render_template('steroids.html', nav=nav, items=items, text=text)

@app.route('/login/', methods=["GET", "POST"])
def login():

    cursor = cnx.cursor()
    cursor.execute("SELECT name, link, image FROM category")
    result = cursor.fetchall()
    cursor.close()
    products = []
    for row in result:
        products.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    registration = NavItem("Регистрация", "/registration/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(registration)
    nav.push(about_us)

    if request.method == "POST":
        cursor = cnx.cursor(buffered=True)
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
            cnx.commit()

            cursor.execute("SELECT token FROM user WHERE id = %s" % res)
            token_from_db = cursor.fetchone()
            resp = make_response(redirect('/'))
            resp.set_cookie('login', '%s' % request.form["login_field"])
            resp.set_cookie('token', '%s' % token_from_db)
            return resp
        else:
            error = "*Данная комбинация логина/пароля введена с ошибкой либо не существует!"
            return render_template("login.html", nav=nav, error=error)
             
    cursor.close()

    return render_template("login.html", nav=nav)

if __name__ == '__main__':
    app.run(debug=True)