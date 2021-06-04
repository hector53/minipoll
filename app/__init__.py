from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = '4as8d4as8d4q848e48a4wd4q348ra48wd48aw48eqw8er'
socketio = SocketIO(app)


from app.request import *
from app.routes import *

