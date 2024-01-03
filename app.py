import logging
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from clients import Clients
from secrets import token_hex

app = Flask(__name__)
app.config["SECRET_KEY"] = token_hex(16)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per second"],
    storage_uri="memory://",
)
socketio = SocketIO(app, cors_allowed_origins="*")
clients = Clients()


@app.route("/")
def index():
    return "<h1>Socket Server Active!</h1>"

if __name__ == "__main__":
    import endpoints.connections as _  # noqa: F401

    socketio.run(app, port=1205, allow_unsafe_werkzeug=True, debug=False) # gunicorn running on server, for testing
