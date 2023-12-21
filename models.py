import sqlite3
import json
from datetime import datetime
from dateutil.parser import parse
from datetime import datetime, timedelta

DATABASE_FILE = 'your_database.db'


class Data:
    def insert_data(self, device_id, state, time, sequence_number, datetime_obj):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            query = '''
                                SELECT * FROM Data
                                WHERE device_id = ?
                                ORDER BY Datetime DESC
                                LIMIT 1
                            '''
            cursor.execute(query, (device_id,))
            latest_data = cursor.fetchone()
            cursor.execute('''
                INSERT INTO Data (device_id, state, time, sequence_number,Datetime)
                VALUES (?, ?, ?, ?, ?)
            ''', (device_id, state, time, sequence_number, datetime_obj))
            conn.commit()

        latest_data_date = parse(latest_data[5])
        time_difference = abs(latest_data_date - datetime_obj)
        treshhold = timedelta(hours=1)
        if time_difference > treshhold and (latest_data[2] == 'READY-IDLE-STARVED' and state == 'READY-IDLE-STARVED'):
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            timedelta_str = "{:02}h {:02}m {:02}s".format(hours, minutes, seconds)
            message = device_id + 'is in ' + state + ' for ' + timedelta_str
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                           INSERT INTO Notification (device_id, message, state, time)
                           VALUES (?, ?, ?, ?)
                       ''', (device_id, message, state, sequence_number, date_string))
            conn.commit()
        pass
    def fetch_robot_ids(self):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT device_id FROM Data ORDER BY device_id ASC")
            robot_ids = [row[0] for row in cursor.fetchall()]
        return robot_ids
    def fetch_all_data(self,robtID,startDate=None,endDate=None):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            if robtID == None:
                if startDate == None:
                    cursor.execute('SELECT * FROM Data')
                else:
                    startDate_obj = parse(startDate)
                    endDate_obj = parse(endDate)
                    cursor.execute('SELECT * FROM Data where Datetime BETWEEN ? AND ?',
                                   ( startDate_obj, endDate_obj))
            else:
                if startDate== None:
                    cursor.execute('SELECT * FROM Data where device_id = ?', (robtID,))
                else:
                    startDate_obj = parse(startDate)
                    endDate_obj = parse(endDate)
                    cursor.execute('SELECT * FROM Data WHERE device_id = ? AND Datetime BETWEEN ? AND ?',
                                   (robtID, startDate_obj, endDate_obj))

            data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        datalist = []
        for row in data:
            d = {
                columns[0]: row[0],
                columns[1]: row[1],
                columns[2]: row[2],
                columns[3]: row[3],
                columns[4]: row[4],
                columns[5]: row[5],
            }
            datalist.append(d)
        datalist = sorted(datalist, key=lambda x: parse(x['Datetime']), reverse=True)
        return datalist

    def rob_data_states(self, robtID):
        data = self.fetch_all_data(robtID)
        start_time =parse(data[-1]["Datetime"])
        end_time = parse(data[0]["Datetime"])
        total_time = (end_time - start_time).total_seconds()
        state_times = {}
        last_record_time = None
        last_record_state = None
        percentage_state_times= {}
        for entry in data:
            state = entry["state"]
            entry_time = parse(entry["Datetime"])
            if last_record_time != None:
                state_times[last_record_state] = state_times.get(last_record_state, 0) + (last_record_time - entry_time).total_seconds()
            last_record_time = entry_time
            last_record_state = state
        percentage_state_times = {state: (time / total_time) * 100 for state, time in state_times.items()}
        return percentage_state_times
    def robots_latast_status(self, robtID):
        data = self.fetch_all_data(robtID)
        latest_record = data[0]
        return latest_record


class Notification:
    @staticmethod
    def insert_notification(message):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Notification (message)
                VALUES (?)
            ''', (message,))
            conn.commit()

    @staticmethod
    def fetch_all_notifications():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Notification')
            return cursor.fetchall()
