# Importē nepieciešamās bibliotēkas
import requests
import json
import datetime
import time
import yaml
import logging
import logging.config
import mysql.connector

from datetime import datetime
from configparser import ConfigParser
from mysql.connector import Error

# Ielādē iepriekš konfigurēto žurnāla konfigurāciju no YAML faila
with open('./log_worker.yaml', 'r') as stream:
    log_config = yaml.safe_load(stream)

logging.config.dictConfig(log_config)

# Izveido žurnāla ierakstītāju
logger = logging.getLogger('root')

# Paziņo par asteroidu apstrādes servisu
logger.info('Asteroid processing service')

# Inicializē un ielādē konfigurācijas vērtības no faila
logger.info('Loading configuration from file')
try:
    config = ConfigParser()
    config.read('config.ini')

    nasa_api_key = config.get('nasa', 'api_key')
    nasa_api_url = config.get('nasa', 'api_url')

    mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
    mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
    mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
    mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')
except:
    logger.exception('')
logger.info('DONE')

# Inicializē datu bāzi
def init_db():
    global connection
    connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)

# Atgriež datu bāzes kursoru
def get_cursor():
    global connection
    try:
        connection.ping(reconnect=True, attempts=1, delay=0)
        connection.commit()
    except mysql.connector.Error as err:
        logger.error("No connection to db " + str(err))
        connection = init_db()
        connection.commit()
    return connection.cursor()

# Pārbauda, vai asteroīds eksistē datu bāzē
def mysql_check_if_ast_exists_in_db(request_day, ast_id):
    records = []
    cursor = get_cursor()
    try:
        cursor = connection.cursor()
        result  = cursor.execute("SELECT count(*) FROM ast_daily WHERE `create_date` = '" + str(request_day) + "' AND `ast_id` = '" + str(ast_id) + "'")
        records = cursor.fetchall()
        connection.commit()
    except Error as e:
        logger.error("SELECT count(*) FROM ast_daily WHERE `create_date` = '" + str(request_day) + "' AND `ast_id` = '" + str(ast_id) + "'")
        logger.error('Problem checking if asteroid exists: ' + str(e))
        pass
    return records[0][0]

# Ievieto asteroīda vērtības datu bāzē
def mysql_insert_ast_into_db(create_date, hazardous, name, url, diam_min, diam_max, ts, dt_utc, dt_local, speed, distance, ast_id):
    cursor = get_cursor()
    try:
        cursor = connection.cursor()
        result  = cursor.execute( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('" + str(create_date) + "', '" + str(hazardous) + "', '" + str(name) + "', '" + str(url) + "', '" + str(diam_min) + "', '" + str(diam_max) + "', '" + str(ts) + "', '" + str(dt_utc) + "', '" + str(dt_local) + "', '" + str(speed) + "', '" + str(distance) + "', '" + str(ast_id) + "')")
        connection.commit()
    except Error as e:
        logger.error( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('" + str(create_date) + "', '" + str(hazardous) + "', '" + str(name) + "', '" + str(url) + "', '" + str(diam_min) + "', '" + str(diam_max) + "', '" + str(ts) + "', '" + str(dt_utc) + "', '" + str(dt_local) + "', '" + str(speed) + "', '" + str(distance) + "', '" + str(ast_id) + "')")
        logger.error('Problem inserting asteroid values into DB: ' + str(e))
        pass

# Pārsūta asteroidu masīvus datu bāzē
def push_asteroids_arrays_to_db(request_day, ast_array, hazardous):
    for asteroid in ast_array:
        if mysql_check_if_ast_exists_in_db(request_day, asteroid[9]) == 0:
            logger.debug("Asteroid NOT in db")
            mysql_insert_ast_into_db(request_day, hazardous, asteroid[0], asteroid[1], asteroid[2], asteroid[3], asteroid[4], asteroid[5], asteroid[6], asteroid[7], asteroid[8], asteroid[9])
        else:
            logger.debug("Asteroid already IN DB")

if __name__ == "__main__":
    connection = None
    connected = False

    init_db()

    # Atver savienojumu ar MySQL datu bāzi
    logger.info('Connecting to MySQL DB')
    try:
        cursor = get_cursor()
        if connection.is_connected():
            db_Info = connection.get_server_info()
            logger.info('Connected to MySQL database. MySQL Server version on ' + str(db_Info))
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            logger.debug('Your connected to - ' + str(record))
            connection.commit()
    except Error as e:
        logger.error('Error while connecting to MySQL' + str(e))

    # Iegūst šodienas datumu
    dt = datetime.now()
    request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)
    logger.debug("Generated today's date: " + str(request_date))

    # Pieprasa informāciju no NASA API
    logger.debug("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))
    r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)
    # Izdrukā NASA piepras
