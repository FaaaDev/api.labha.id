from flask import jsonify


class response:
    def __new__(self, code, message, status, data):
        return (
            jsonify({"code": code, "status": status, "message": message, "data": data}),
            code,
        )
