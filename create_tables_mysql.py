import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root",
                                  password="P@ssw0rd", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
                  CREATE TABLE renting_request           
                  (id INT NOT NULL AUTO_INCREMENT, 
                    user_id INTEGER NOT NULL,
                    user_device_id INTEGER NOT NULL,
                    charging_box_id VARCHAR(250) NOT NULL,
                    timestamp VARCHAR(100) NOT NULL,
                    date_created VARCHAR(100) NOT NULL,
                    CONSTRAINT renting_request_pk PRIMARY KEY (id))
                  ''')

db_cursor.execute('''
                  CREATE TABLE charging_box_status           
                  (id INT NOT NULL AUTO_INCREMENT, 
                    charging_box_id VARCHAR(250) NOT NULL,
                    power_banks_remain INTEGER NOT NULL,
                    power_bank_id VARCHAR(250) NOT NULL,
                    battery_level INTEGER NOT NULL,
                    timestamp VARCHAR(100) NOT NULL,
                    date_created VARCHAR(100) NOT NULL,
                    CONSTRAINT charging_box_status_pk PRIMARY KEY (id))
                  ''')

db_conn.commit()
db_conn.close()
