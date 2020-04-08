from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RentingRequest(Base):
    """ Renting Request """

    __tablename__ = "renting_request"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    user_device_id = Column(Integer, nullable=False)
    charging_box_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, user_id, user_device_id, charging_box_id, timestamp):
        """ Initializes a blood pressure reading """
        self.user_id = user_id
        self.user_device_id = user_device_id
        self.charging_box_id = charging_box_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['user_device_id'] = self.user_device_id
        dict['charging_box_id'] = self.charging_box_id
        dict['timestamp'] = self.timestamp

        return dict
