import json
import threading
import paho.mqtt.subscribe as subscribe
from models import Data
from initialization import initialize_database
from dateutil.parser import parse

Data_obj = Data()


class DataService:
    def initialize_database(self):
        initialize_database()

    def insert_data(self, device_id, state, time, sequence_number, datetime_object):
        Data_obj.insert_data(device_id, state, time, sequence_number, datetime_object)

    def fetch_robot_ids(self):
        return Data_obj.fetch_robot_ids()

    def fetch_all_data(self, robtID=None, startDate=None, endDate=None):
        return json.dumps(Data_obj.fetch_all_data(robtID, startDate, endDate))

    def insert_notification(
        self,
        device_id,
        state,
        time,
        sequence_number,
        datetime_object,
        last_record,
        last_state,
    ):
        Data_obj.insert_notification(
            device_id,
            state,
            time,
            sequence_number,
            datetime_object,
            last_record,
            last_state,
        )

    def fetch_all_notifications(self, robtID=None, startDate=None, endDate=None):
        return json.dumps(Data_obj.fetch_all_notifications(robtID, startDate, endDate))

    def rob_data_stats(self, robtID=None):
        return json.dumps(Data_obj.rob_data_states(robtID))

    def robots_latast_status(self, robtID=None):
        return json.dumps(Data_obj.robots_latast_status(robtID))


class MQTTService:
    def __init__(self, data_service):
        self.data_service = data_service
        self.x = threading.Thread()

    def on_message_insert_db(self, client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            data = json.loads(payload)
            device_id = data.get("deviceId", "")
            state = data.get("state", "")
            time = data.get("time", "")
            sequence_number = data.get("sequenceNumber", "")
            datetime_object = parse(time)
            last_record = json.loads(self.data_service.robots_latast_status(device_id))
            self.data_service.insert_data(
                device_id, state, time, sequence_number, datetime_object
            )
            last_state = last_record["state"]
            self.data_service.insert_notification(
                device_id,
                state,
                time,
                sequence_number,
                datetime_object,
                last_record,
                last_state,
            )

            print(
                f"Received message for {device_id}: State={state}, Time={time}, Sequence Number={sequence_number}"
            )
        except Exception as e:
            if payload == "Test":
                pass
            else:
                print(f"Error processing message: {e}")

    def start_mqtt_subscription(self, data_service):
        if self.x.is_alive():
            print("Thread is already started.")
            return "Thread is already started."
        else:
            data_service.initialize_database()
            self.x = threading.Thread(
                target=subscribe.callback,
                args=(self.on_message_insert_db, "ii23/telemetry/#"),
                kwargs={"hostname": "broker.mqttdashboard.com"},
            )
            self.x.start()
            return "Starting threads"
