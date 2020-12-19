import mysql.connector


myconn = mysql.connector.connect(
        user='root',
        host='35.184.114.147',
        passwd='vIODkJMsnnjPm4gO',
        database='scraping_master',
        charset='utf8',
        auth_plugin='mysql_native_password'
        )

cursor = myconn.cursor()

def get_news():
    result = {}

    sql = 'SELECT title, overview, url, body, pub_date FROM articles ORDER BY pub_date LIMIT 6'
    try:
        response = cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        myconn.close()
        return result

