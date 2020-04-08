from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class ChargingBoxStatus(Base):
    """ Heart Rate """

    __tablename__ = "charging_box_status"

    id = Column(Integer, primary_key=True)
    charging_box_id = Column(String(250), nullable=False)
    power_banks_remain = Column(Integer, nullable=False)
    power_bank_id = Column(String(100), nullable=False)
    battery_level = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, charging_box_id, power_banks_remain, power_bank_id, battery_level, timestamp):
        """ Initializes a heart rate reading """
        self.charging_box_id = charging_box_id
        self.power_banks_remain = power_banks_remain
        self.power_bank_id = power_bank_id
        self.battery_level = battery_level
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['charging_box_id'] = self.charging_box_id
        dict['power_banks_remain'] = self.power_banks_remain
        dict['power_bank_status'] = {}
        dict['power_bank_status']['power_bank_id'] = self.power_bank_id
        dict['power_bank_status']['battery_level'] = self.battery_level
        dict['timestamp'] = self.timestamp

        return dict
