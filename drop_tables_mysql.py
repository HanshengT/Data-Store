import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root",
                                  password="P@ssw0rd", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
                   DROP TABLE renting_request, charging_box_status
                   ''')

db_conn.commit()
db_conn.close()