from quart import Quart

application = app = Quart(__name__)


@app.route('/api/v1/user/register', methods=['POST'])
async def register():
    pass


@app.route('/api/v1/user/auth', methods=['POST'])
async def auth():
    pass


@app.route('/api/v1/user/get-kins', methods=['POST'])
async def get_kins():
    pass


@app.route('/api/v1/server-wallet', methods=['POST'])
async def get_cwpa():
    pass


@app.route('/api/v1/user/history', methods=['POST'])
async def history():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8000)
