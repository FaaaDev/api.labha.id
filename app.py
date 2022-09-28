from main import app
from sshtunnel import SSHTunnelForwarder
import time
from threading import Thread
from flask_cors import CORS
from os.path import join, dirname, realpath
from main.shared.shared import db, ma

server = SSHTunnelForwarder(
    ("103.179.56.92", 22),
    ssh_username="andynoer",
    ssh_password="Kulonuwun450",
    remote_bind_address=("127.0.0.1", 5432),
)

server.start()

def db_server():
    servers = server
    uptime = 0
    while True:
        if servers.is_active:
            minutes=(uptime/(60))%60
            hours=(uptime/(60*60))%24
            days=(uptime/(60*60*24))%1
            print("Uptime: %d days %d hours %d minutes" %(int(days), int(hours), int(minutes)))
        else:
            print("reconnecting... " + time.ctime())
            servers.stop()
            servers = SSHTunnelForwarder(
                ("103.179.56.92", 22),
                ssh_username="andynoer",
                ssh_password="Kulonuwun450",
                remote_bind_address=("127.0.0.1", 5432),
            )
            servers.start()

            app.config["SQLALCHEMY_DATABASE_URI"] = (
                "postgresql://postgres:12345678@127.0.0.1:"
                + str(servers.local_bind_port)
                + "/acc_dev"
            )

        uptime += 60
        time.sleep(60)


Thread(target=db_server, daemon=True).start()


app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:12345678@127.0.0.1:"
    + str(server.local_bind_port)
    + "/acc_dev"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["JSON_SORT_KEYS"] = False
app.config["UPLOAD_FOLDER"] = join(dirname(realpath(__file__)), "static/upload")
app.config[
    "SECRET_KEY"
] = "IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu"
app.secret_key = "IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu"
CORS(app)


db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
