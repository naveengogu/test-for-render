from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'corona-virus-report', 'full_grouped.csv')

df = pd.read_csv(DATA_PATH)

app = Flask(__name__)
CORS(app)

@app.route('/api/countries')
def get_countries():
    countries = sorted(df['Country/Region'].unique().tolist())
    return jsonify({'countries': countries})

@app.route('/api/country/<country>')
def get_country_data(country):
    country_df = df[df['Country/Region'] == country]
    if country_df.empty:
        return jsonify({'error': 'Country not found'}), 404
    data = {
        'date': country_df['Date'].tolist(),
        'confirmed': country_df['Confirmed'].tolist(),
        'deaths': country_df['Deaths'].tolist(),
        'recovered': country_df['Recovered'].tolist(),
        'active': country_df['Active'].tolist(),
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True) 