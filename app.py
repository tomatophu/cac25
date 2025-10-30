from base64 import b64encode

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS


# Setup 
app = Flask(__name__)
CORS(app)


# API
@app.route('/events/create', methods=['POST'])
def create_event():
    if image := request.files.get("image"):
        image = b64encode(image.read()).decode("utf-8")

    with open('src/data/my_event.txt', 'a') as file:
        file.write(f'title: {request.form.get("name")} \n')
        file.write(f'time: {request.form.get("time")} \n')
        file.write(f'location: {request.form.get("location1")} {request.form.get("location2")} \n')
        file.write(f'details: {request.form.get("details")} \n')
        file.write(f'image: {image} \n')
        file.write(f'creator: {request.form.get("creator")} \n')
        file.write('--- \n')
    
    return jsonify({
        'message': 'Event created successfully',
    }), 200

@app.route('/account/create', methods=['POST'])
def create_account():
    with open('src/data/account.txt', 'a') as file:
        file.write(f'username: {request.form.get("username")} \n')
        file.write(f'email: {request.form.get("email")} \n')
        file.write(f'password: {request.form.get("password")} \n')
        file.write('--- \n')

    return jsonify({
        'message': 'Account created successfully',
    }), 200

@app.route('/account/login', methods=['POST'])
def login_account():
    with open('src/data/account.txt', 'r') as file:
        accounts = file.read().split('---')[:-1]
        for account in accounts: 
            data = {}
            # Remove whitespace lines
            for field in filter(lambda x: x.strip(), account.splitlines()):
                split = field.split(':')
                data[split[0].strip()] = split[1].strip()
            if (data['username'] == request.form.get('username')
                and data['password'] == request.form.get('password')):
                return jsonify({
                    'message': 'Credentials are valid',
                }), 200

    return jsonify({
        'message': 'I am a teapot',
    }), 418


# Run
if __name__ == '__main__':
    app.run(debug=1)

