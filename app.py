from flask import Flask, render_template, request
from controllers import DataService, MQTTService
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/data": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'


@app.route('/')
def display_data():
    data = data_service.fetch_all_data()
    robot_ids = data_service.fetch_robot_ids()
    default_robot_id = 'rob1'
    return render_template('dashboard.html', data=data, robot_ids=robot_ids, nID=default_robot_id)


@app.route('/measurement-history')
def display_measurement_data():
    data = data_service.fetch_all_data()
    robot_ids = data_service.fetch_robot_ids()
    default_robot_id = 'rob1'
    return render_template('measurement-history.html', data=data, robot_ids=robot_ids, nID=default_robot_id)


@app.route('/event-history')
def display_event_data():
    data = data_service.fetch_all_data()
    robot_ids = data_service.fetch_robot_ids()
    return render_template('event-history.html', data=data, robot_ids=robot_ids)


@app.route('/data')
def data():
    robtID = request.args.get('robtID', default=None)
    startDate = request.args.get('startDate', default=None)
    endDate = request.args.get('endDate', default=None)
    data = data_service.fetch_all_data(robtID, startDate, endDate)
    return data

@app.route('/Alarms')
def Alarms():
    robtID = request.args.get('robtID', default=None)
    startDate = request.args.get('startDate', default=None)
    endDate = request.args.get('endDate', default=None)
    data = data_service.fetch_all_notifications(robtID, startDate, endDate)
    return data
@app.route('/rob_data_stats')
def get_robot():
    robtID = request.args.get('robtID', default=None)
    data = data_service.rob_data_stats(robtID)
    return data


@app.route('/robots_latest_status')
def get_robot_latast_status():
    robtID = request.args.get('robtID', default=None)
    data = data_service.robots_latast_status(robtID)
    return data


data_service = DataService()
mqtt_service = MQTTService(data_service)
message = mqtt_service.start_mqtt_subscription(data_service)
print(message)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
