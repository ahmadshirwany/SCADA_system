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
            print("********************* Data added ************************************")
        pass

    def fetch_robot_ids(self):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT device_id FROM Data ORDER BY device_id ASC")
            robot_ids = [row[0] for row in cursor.fetchall()]
        return robot_ids

    def fetch_all_data(self, robtID, startDate=None, endDate=None):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            if robtID == None:
                if startDate == None:
                    cursor.execute('SELECT * FROM Data')
                else:
                    startDate_obj = parse(startDate)
                    endDate_obj = parse(endDate)
                    cursor.execute('SELECT * FROM Data where Datetime BETWEEN ? AND ?',
                                   (startDate_obj, endDate_obj))
            else:
                if startDate == None:
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
                columns[3]: parse(row[3]).strftime("%Y-%m-%d %H:%M:%S"),
                columns[4]: row[4],
                columns[5]: row[5],
            }
            datalist.append(d)
        datalist = sorted(datalist, key=lambda x: parse(x['Datetime']), reverse=True)
        return datalist

    def rob_data_states(self, robtID):
        data = self.fetch_all_data(robtID)
        start_time = parse(data[-1]["Datetime"])
        end_time = parse(data[0]["Datetime"])
        total_time = (end_time - start_time).total_seconds()
        state_times = {}
        last_record_time = None
        last_record_state = None
        percentage_state_times = {}
        for entry in data:
            state = entry["state"]
            entry_time = parse(entry["Datetime"])
            if last_record_time != None:
                state_times[last_record_state] = state_times.get(last_record_state, 0) + (
                        last_record_time - entry_time).total_seconds()
            last_record_time = entry_time
            last_record_state = state
        percentage_state_times = {state: (time / total_time) * 100 for state, time in state_times.items()}
        return percentage_state_times

    def get_mtbf(self, robtID):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Data where state = ?', ('DOWN',))
            cursor.execute('SELECT * FROM Data WHERE device_id = ? AND state = ?', (robtID, 'DOWN'))
            data = cursor.fetchall()
            if len(data)>1:
                time_objects = [parse(log[3]) for log in data]
                time_objects.sort()
                time_diffs = [time_objects[i] - time_objects[i - 1] for i in range(1, len(time_objects))]
                total_time_diff = sum(time_diffs, timedelta())
                total_time_diff_seconds = total_time_diff.total_seconds()
                average_time_diff_seconds = total_time_diff_seconds / len(time_diffs)
                time_difference = timedelta(seconds=average_time_diff_seconds)
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                average_time_diff = "{:02d} hrs {:02d} min {:02d} sec".format(hours, minutes, seconds)
                # average_time_diff = str(timedelta(seconds=average_time_diff_seconds))
            else:
                average_time_diff = 'NA'
        return average_time_diff

    def robots_latast_status(self, robtID):
        data = self.fetch_all_data(robtID)
        latest_record = data[0]
        mtbf = self.get_mtbf(latest_record['device_id'])
        latest_record['meandata'] = mtbf
        return latest_record

    def insert_notification(self, device_id, state, time, sequence_number, datetime_object, last_state):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            if state == "DOWN":
                timestamp = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                message = f"At {timestamp}, Device {device_id} state changed to {state}."
            else:
                timestamp = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                message = f"At {timestamp}, Device {device_id} state changed to {state} from {last_state}."
            cursor.execute('''
                INSERT INTO Notification (device_id, message, state, time)
                VALUES (?,?,?,?)
            ''', (device_id, message, state, datetime_object))
            conn.commit()

    def fetch_all_notifications(self, robtID, startDate=None, endDate=None):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            if robtID == None:
                if startDate == None:
                    cursor.execute('SELECT * FROM Notification')
                else:
                    startDate_obj = parse(startDate)
                    endDate_obj = parse(endDate)
                    cursor.execute('SELECT * FROM Notification where time BETWEEN ? AND ?',
                                   (startDate_obj, endDate_obj))
            else:
                if startDate == None:
                    cursor.execute('SELECT * FROM Notification where device_id = ?', (robtID,))
                else:
                    startDate_obj = parse(startDate)
                    endDate_obj = parse(endDate)
                    cursor.execute('SELECT * FROM Notification WHERE device_id = ? AND time BETWEEN ? AND ?',
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
            }
            datalist.append(d)
        datalist = sorted(datalist, key=lambda x: parse(x['time']), reverse=True)
        return datalist
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Notification')
            return cursor.fetchall()
