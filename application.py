from flask import Flask

application = app = Flask(__name__)


@app.route('/api/v1/user/register', methods=['POST'])
def register():
    pass


@app.route('/api/v1/user/auth', methods=['POST'])
def auth():
    pass


@app.route('/api/v1/user/get-kins', methods=['POST'])
def auth():
    pass


@app.route('/api/v1/user/history', methods=['POST'])
def auth():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8000)
