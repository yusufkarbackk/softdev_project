from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
import urllib.request
import requests
import datetime
import json
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menus/')
def menus():
    return render_template('menus.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        requests.post(
            'https://67c7-139-193-225-168.ap.ngrok.io/users/register', json=data)
    return render_template('register.html')


def set_cookie(response, token):
    response.set_cookie('jwt_token', token, expires=datetime.datetime.utcnow(
    ) + datetime.timedelta(days=1), httponly=True)
    return jsonify(response)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        token = requests.post(
            'https://67c7-139-193-225-168.ap.ngrok.io/login/token', json=data)
        print(token.text)

        response = make_response(render_template('index.html'))

        response.set_cookie('jwt_token', token.text, expires=datetime.datetime.utcnow(
        ) + datetime.timedelta(days=1), httponly=True)
        return response
    return render_template('login.html')


@app.route('/jobs/')
def jobs():
    cookie_value = request.cookies.get('jwt_token')
    print(cookie_value)

    header = {'Authorization': f'Bearer {cookie_value}'}

    jobs = requests.get(
        'https://67c7-139-193-225-168.ap.ngrok.io/jobs/all', headers=header)
    print(type(json.loads(jobs.text)))
    
    data = json.loads(jobs.text)
    
    print(data)
    return render_template('menus.html', menus=data)


if __name__ == '__main__':
    app.run(debug=True)
