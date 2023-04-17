import time
import os
from main import app, db, ma
from sshtunnel import SSHTunnelForwarder
from threading import Thread
from flask_cors import CORS
from os.path import join, dirname, realpath
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

server = SSHTunnelForwarder(
    (os.getenv('SSH_HOST'), 22),
    ssh_username=os.getenv('SSH_USER'),
    ssh_password=os.getenv('SSH_PASSWORD'),
    remote_bind_address=("127.0.0.1", 5432),
)

server.start()


def db_server():
    servers = server
    uptime = 0
    while True:
        if servers.is_active:
            minutes = (uptime/(60)) % 60
            hours = (uptime/(60*60)) % 24
            days = (uptime/(60*60*24)) % 1
            print("Uptime: %d days %d hours %d minutes" %
                  (int(days), int(hours), int(minutes)))
        else:
            print("reconnecting... " + time.ctime())
            servers.stop()
            servers = SSHTunnelForwarder(
                (os.getenv('SSH_HOST'), 22),
                ssh_username=os.getenv('SSH_USER'),
                ssh_password=os.getenv('SSH_PASSWORD'),
                remote_bind_address=("127.0.0.1", 5432),
            )
            servers.start()

            app.config["SQLALCHEMY_DATABASE_URI"] = (
                "postgresql://%s:%s@127.0.0.1:" % (
                    os.getenv('DB_USER'), os.getenv('DB_PASSWORD')
                )
                + str(servers.local_bind_port)
                + "/%s" % (os.getenv('DB_NAME'))
            )

        uptime += 60
        time.sleep(60)


Thread(target=db_server, daemon=True).start()


app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://%s:%s@127.0.0.1:" % (
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD')
    )
    + str(server.local_bind_port)
    + "/%s" % (os.getenv('DB_NAME'))
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["JSON_SORT_KEYS"] = False
app.config["UPLOAD_FOLDER"] = join(
    dirname(realpath(__file__)), "static/upload")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)


db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv('PORT'))
