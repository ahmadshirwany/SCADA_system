from flask import Flask, render_template, request
from controllers import  DataService,MQTTService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

@app.route('/')
def display_data():
    data = data_service.fetch_all_data()
    return render_template('index.html', data=data)


@app.route('/data')
def data():
    robtID = request.args.get('robtID', default=None)
    data = data_service.fetch_all_data(robtID)
    return data

@app.route('/rob_data_stats')
def get_robot():
    robtID = request.args.get('robtID', default=None)
    data = data_service.rob_data_stats(robtID)
    return data

@app.route('/robots_latest_statu')
def get_robot_latast_status():
    robtID = request.args.get('robtID', default=None)
    data = data_service.robots_latast_status(robtID)
    return data


# @app.route('/start')
# def start_tread():
#     message = mqtt_service.start_mqtt_subscription()
#     return message

data_service = DataService()
mqtt_service = MQTTService(data_service)
message = mqtt_service.start_mqtt_subscription(data_service)
print(message)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')