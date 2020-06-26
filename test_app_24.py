from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=763d40c11d6ddf5d7ffd281cd6ec37d2'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


if __name__ == "__main__":
    # app.debug = True
    app.run(debug=True)
    # app.run()


# @app.route('/<city1>', methods=['GET', 'POST'])
# def index(city1):
#     if request.method == "GET":
#         city = city1
#
#         url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=763d40c11d6ddf5d7ffd281cd6ec37d2'
#
#         weather_data = []
#         res = requests.get(url.format(city)).json()
#         # for city in cities:
#         #     res = requests.get(url.format(city.name)).json()
#
#         weather = {
#                 'city': city,
#                 'temperature': res['main']['temp'],
#                 'description': res['weather'][0]['description'],
#                 'icon': res['weather'][0]['icon'],
#             }
#
#         weather_data.append(weather)
#
#         return render_template('weather.html', weather_data=weather_data)
#         # return res
#     elif request.method == "POST":
#         weather_data = []
#         url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=763d40c11d6ddf5d7ffd281cd6ec37d2'
#         if city1:
#             new_city = City(name=city1)
#
#             db.session.add(new_city)
#             db.session.commit()
#
#         cities = City.query.all()
#         for city in cities:
#             res = requests.get(url.format(city.name)).json()
#
#         weather = {
#             'city': city1,
#             'temperature': res['main']['temp'],
#             'description': res['weather'][0]['description'],
#             'icon': res['weather'][0]['icon'],
#         }
#
#         weather_data.append(weather)
#
#         # return render_template('weather.html', weather_data=weather_data)
#
#         return 201

# return res

# @app.route('/')
# def hello():
#     print("Hi Rishi")
#     return 'RK is GENIUS'

# @app.route('/')
# def hello():
#     print("Hi Rishi")
#     return 'RK is GENIUS'
#
#
# @app.route('/age/<int:pid>')
# def age(pid):
#     return 'Your age is %d' % pid
#
#
# @app.route('/sal/<float:snm>')
# def salary(snm):
#     return 'Your monthly sal soon will be %f ' % snm
#
#

