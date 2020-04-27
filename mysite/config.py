import os


DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASSWORD = os.getenv('DB_PASSWORD')
if DB_LOGIN == None:
    print('Set database login into Environment Variables!')
    exit(1)
elif DB_PASSWORD == None:
    print('Set database password into Environment Variables!')
    exit(1)


DB_HOST = '127.0.0.1'
DB_NAME = 'shop_db'