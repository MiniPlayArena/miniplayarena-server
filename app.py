from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from clients import Clients

app = Flask(__name__)
app.config["SECRET_KEY"] = "cum-monster"
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per second"], storage_uri="memory://")
clients = Clients()
socketio = SocketIO(app)

if __name__ == "__main__":
    from endpoints.auth import new_game
    app.register_blueprint(new_game)
    
    socketio.run(app, port=696, host="0.0.0.0", debug=True)