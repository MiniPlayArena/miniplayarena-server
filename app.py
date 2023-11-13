import logging
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from clients import Clients

app = Flask(__name__)
app.config["SECRET_KEY"] = "cum-monster"

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
    return "<h1>kushy wushy >~<</h1>"

if __name__ == "__main__":
    import endpoints.connections as _  # noqa: F401

    socketio.run(app, port=696, host="0.0.0.0", debug=False)
