from ..utils.response import response
from ..shared.shared import db
from sqlalchemy import text
import requests


class UpdateTable:
    def __new__(self, model, request):

        updated = []
        db.session.rollback()

        if type(model) == list:
            for x in model:
                sql = text(
                    "select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME= '%s' and TABLE_SCHEMA = '%s'"
                    % (x.__tablename__, x.__table_args__["schema"])
                )

                real_table = db.session.execute(sql)

                real_column = []

                for z in real_table.mappings().all():
                    real_column.append(z["column_name"])

                for c in x.__table__.columns:
                    if c.name not in real_column:
                        updated.append("%s.%s" % (x.__tablename__, c.name))
                        sql = text(
                            (
                                'ALTER TABLE "%s"."%s" ADD %s %s NULL'
                                % (
                                    x.__table_args__["schema"],
                                    x.__tablename__,
                                    c.name,
                                    c.type,
                                )
                            )
                            + (" DEFAULT %s" % (c.default) if c.default else "")
                        )

                        print(sql)

                        db.session.execute(sql)

                db.session.commit()
        else:
            sql = text(
                "select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME= '%s' and TABLE_SCHEMA = '%s'"
                % (model.__tablename__, model.__table_args__["schema"])
            )
            real_table = db.session.execute(sql)

            real_column = []

            for x in real_table.mappings().all():
                real_column.append(x["column_name"])

            for c in model.__table__.columns:
                if c.name not in real_column:
                    updated.append("%s.%s" % (model.__tablename__, c.name))
                    sql = text(
                        (
                            "ALTER TABLE %s.%s ADD %s %s NULL"
                            % (
                                model.__table_args__["schema"],
                                model.__tablename__,
                                c.name,
                                c.type,
                            )
                        )
                        + (" DEFAULT %s" % (c.default) if c.default else "")
                    )
                    db.session.execute(sql)

            db.session.commit()

        # print(request.url)
        # print(request.headers)
        # print(request.method)

        if request.method == "POST":
            result = requests.post(
                url=request.url, headers=request.headers, json=request.json
            ).json()
        elif request.method == "GET":
            result = requests.get(
                url=request.url, headers=request.headers).json()
        elif request.method == "PUT":
            result = requests.put(
                url=request.url, headers=request.headers, json=request.json
            ).json()
        elif request.method == "DELETE":
            result = requests.delete(
                url=request.url, headers=request.headers).json()

        return response(
            200,
            "Table %s Updated!" % (",".join(updated)),
            result["status"],
            result["data"],
        )
