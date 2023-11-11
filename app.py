import pusher
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per second"], storage_uri="memory://")
pusher = pusher.Pusher(
    app_id = "1706778",
    key = "7ccf4bc1ee9c8d02d536",
    secret = "e7663f8d9b97f6442b07",
    cluster = "eu"
)
# pusher.trigger(u"test-uno", u"init", {u"users": [u"user-1", u"user-2"]})

if __name__ == "__main__":
    from endpoints.auth import auth
    app.register_blueprint(auth)
    
    app.run(port=696, host="0.0.0.0")