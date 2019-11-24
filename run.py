from flask import Flask, render_template, request
from classes import*
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', password='Dianabol250', host='127.0.0.1', database='shop_db')

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
        user_info = (request.form['user_login'], request.form['user_name'], request.form['user_surname'], request.form['user_email'], request.form['user_mobilenumber'], request.form['user_dob'], request.form['user_town'], request.form['user_pass'])
        print(user_info)
        try:
            cursor = cnx.cursor(buffered=True)
            data_check = (request.form['user_login'],request.form['user_email'],)
            query_from_db = "SELECT login, email FROM user WHERE login = %s OR email = %s"        
            sql = "INSERT INTO user (login, name, surname, email, mobilenumber, dob, town, password) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            check = cursor.execute(query_from_db, data_check)
            print(check)
            if check == None:
                cursor.execute(sql, user_info)
                cnx.commit()
            else:
                cnx.rollback()
                error = "Данный логин либо электронная почта уже зарегестрированы на данном сайте!"



        except mysql.connector.Error as err:
            print(err)
            error = "Данный логин либо электронная почта уже зарегестрированы на данном сайте! Попробуйте еще раз!"
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




if __name__ == '__main__':
    app.run(debug=True)