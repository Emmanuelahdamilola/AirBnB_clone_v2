from flask import Flask, render_template

app = Flask(__name__)

# Set strict_slashes to False
app.url_map.strict_slashes = False

@app.route('/')
def home():
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
