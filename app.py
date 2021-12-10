import json

from flask import Flask, render_template, session

from auth_user.routes import login_app
from basket.routes import basket_app
from requests.routes import user_app

app = Flask(__name__)

app.register_blueprint(user_app, url_prefix='/requests')
app.register_blueprint(login_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')


app.config['DB_CONFIG'] = json.load(open('configs/db.json', 'r'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json', 'r'))
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/clear-session')
def clear_session():
    session.clear()
    return render_template('exit.html')


if (__name__ == "__main__"):
    app.run(host="127.0.0.1", port=9000, debug=True)