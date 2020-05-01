from mysite import config
import mysql.connector


def do_database_connection(config):
	cnx = mysql.connector.connect(user=config.DB_LOGIN, password=config.DB_PASSWORD, host=config.DB_HOST, database=config.DB_NAME)
	cnx.autocommit = False
	return cnx

cnx = do_database_connection(config)