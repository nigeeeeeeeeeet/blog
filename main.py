from flask import Flask, render_template

import settings
from db_scripts import get_user

app = Flask(__name__)
app.config.from_object(settings)
app.secret_key = settings.SECRET_KEY


@app.route('/')
@app.route('/index')
def index():
    user = get_user()
    return render_template('index.html', user=user)


@app.route('/about')
def about():
    user = get_user()
    return render_template('about.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
