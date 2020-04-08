import connexion

from connexion import NoContent
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from renting_request import RentingRequest
from charging_box_status import ChargingBoxStatus
import datetime
from threading import Thread
from pykafka import KafkaClient
import json


with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' +
                          app_config['datastore']['password'] + '@' + app_config['datastore']['hostname'] + ':' +
                          str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])

DB_SESSION = sessionmaker(bind=DB_ENGINE)


"""def report_renting_request(rentingRequest):

    session = DB_SESSION()

    bp = RentingRequest(rentingRequest['user_id'],
                        rentingRequest['user_device_id'],
                        rentingRequest['charging_box_id'],
                        rentingRequest['timestamp'],)

    session.add(bp)

    session.commit()
    session.close()

    return NoContent, 201
"""

def get_renting_request(startDate, endDate):
    """ Get blood pressure reports from the data store """

    results_list = []

    session = DB_SESSION()

    start = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    results = session.query(RentingRequest).filter(RentingRequest.date_created.between(start, end))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200


"""def report_charging_box_status(chargingBoxStatus):

    session = DB_SESSION()

    hr = ChargingBoxStatus(chargingBoxStatus['charging_box_id'],
                           chargingBoxStatus['power_banks_remain'],
                           chargingBoxStatus['power_bank_status']['power_bank_id'],
                           chargingBoxStatus['power_bank_status']['battery_level'],
                           chargingBoxStatus['timestamp'])

    session.add(hr)

    session.commit()
    session.close()

    return NoContent, 201
"""

def get_charging_box_status(startDate, endDate):
    """ Get heart rate reports from the data store """

    results_list = []

    session = DB_SESSION()

    start = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    results = session.query(ChargingBoxStatus).filter(ChargingBoxStatus.date_created.between(start, end))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200


def process_messages():

    client = KafkaClient(hosts=app_config['kafka']['server'] + ':' + str(app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]
    consumer = topic.get_simple_consumer(consumer_group='events', auto_commit_enable=True, auto_commit_interval_ms=100)

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg_dict = json.loads(msg_str)
        if msg_dict['type'] == 'rr':
            session = DB_SESSION()
            msg = msg_dict['payload']
            rr = RentingRequest(msg['user_id'],
                        msg['user_device_id'],
                        msg['charging_box_id'],
                        msg['timestamp'])
            session.add(rr)
            session.commit()
            session.close()
        elif msg_dict['type'] == 'cbs':
            session = DB_SESSION()
            msg = msg_dict['payload']
            cbs = ChargingBoxStatus(msg['charging_box_id'],
                           msg['power_banks_remain'],
                           msg['power_bank_status']['power_bank_id'],
                           msg['power_bank_status']['battery_level'],
                           msg['timestamp'])
            session.add(cbs)
            session.commit()
            session.close()
        else:
            print("Type not found")


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    # run our standalone gevent server
    app.run(port=8090)




