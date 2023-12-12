#!/usr/bin/python3
"""
Starts a Flask web app.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'

@app.route('/hbnb')
def display_hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'

@app.route('/c/<text>')
def display_c(text):
    """Displays 'C' followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.url_map.strict_slashes = False
