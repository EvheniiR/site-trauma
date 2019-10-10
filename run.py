from flask import Flask, render_template
from classes import*
import mysql.connector

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', password='Dianabol250', host='127.0.0.1', database='shop_db')


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
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(0)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)
    return render_template('index.html', products=products, nav=nav)

@app.route('/productlist/')
def productlist():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, about, image FROM product")
    result = cursor.fetchall()
    cursor.close()
   
    items = []
    for row in items:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(1)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)
    return render_template('productlist.html', items=items, nav=nav)

@app.route('/certificates/')
def certificates():
    cursor = cnx.cursor()
    cursor.execute("SELECT name, image FROM certificate")
    result = cursor.fetchall()
    cursor.close()
       
    items = []
    for row in items:
        items.append(Product.from_db_row(row))

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(2)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = "В подтвержение качества и подлинности нашей продукции для Вас мы разместили сертифкаты и свидетельства о госрегистрации."

    return render_template("certificates.html", items=items, nav=nav, text=text)

@app.route('/aboutus/')
def aboutus():

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation(3)

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    return render_template("aboutus.html", nav=nav)

@app.route('/proteins/')
def proteins():

    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)
    text = 'У нас вы можете заказать протеины ведущих фирм премиум-качества.'
    return render_template('proteins.html', nav=nav, items=items, text=text)

@app.route('/gainers/')
def gainers():
    
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")
    
    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = 'У нас вы можете заказать гейнеры ведущих фирм премиум-качества.'

    return render_template('gainers.html', nav=nav, items=items, text=text)

@app.route('/aminoacids/')
def aminoacids():
   
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные аминокислоты ведущих фирм премиум-качества.'

    return render_template('aminoacids.html', nav=nav, items=items, text=text)

@app.route('/creatine/')
def creatine():
    
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = 'У нас Вы можете креатин ведущих фирм премиум-качества.'

    return render_template('creatine.html', nav=nav, items=items, text=text)

@app.route('/burnfats/')
def burnfats():
   
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = 'У нас Вы можете заказать жиросжигатели ведущих фирм премиум-качества.'

    return render_template('burnfats.html', nav=nav, items=items, text=text)

@app.route('/vitamins/')
def vitamins():
    
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = 'У нас Вы можете заказать как комплексные, так и отдельные витамины ведущих фирм премиум-качества.'

    return render_template('vitamins.html', nav=nav, items=items, text=text)

@app.route('/steroids/')
def steroids():
    
    items = []

    home = NavItem( "Домашняя страница", "/")
    product_list = NavItem( "Список товаров сайта", "/productlist/")
    sertification = NavItem( "Сертификаты продукции", "/certificates/")
    about_us = NavItem( "О нас", "/aboutus/")

    nav = Navigation("None")

    nav.push(home)
    nav.push(product_list)
    nav.push(sertification)
    nav.push(about_us)

    text = "У нас Вы можете заказать как комплексные, так и отдельные 'витамины' ведущих фирм премиум-качества."

    return render_template('steroids.html', nav=nav, items=items, text=text)




if __name__ == '__main__':
    app.run(debug=True)