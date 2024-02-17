from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city):
    api_key = '033f19189a8ab629d8ac47ab098e86ef'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == 200:
            weather_info = {
                'Temperature': data['main']['temp'],
                'Humidity': data['main']['humidity'],
                'Description': data['weather'][0]['description']
            }
            return weather_info
        else:
            return {'Error': data['message']}
    except requests.exceptions.RequestException as e:
        return {'Error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_info = get_weather(city_name)
        return render_template('index.html', city=city_name, weather_info=weather_info)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
