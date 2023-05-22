from ...function.update_table import UpdateTable
from sqlite3 import *
from ...model.currency_mdb import CurrencyMdb
from ...model.currency_ddb import CurrencyDdb
from ...shared.shared import db
from ...utils.response import response
from ...schema.currency_mdb import currencys_schema, currency_schema


class Currency:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                name = request.json["name"]
                date = request.json["date"]
                rate = request.json["rate"]
                curren = CurrencyMdb(code, name, date, rate, user.company)
                
                db.session.add(curren)
                db.session.commit()

                new_history = CurrencyDdb(
                    curren.id, request.json["date"], request.json["rate"], curren.comp_id
                )
                db.session.add(new_history)
                db.session.commit()
                
                
            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, currency_schema.dump(curren))
        else:
            try:
                result = CurrencyMdb.query.all()

                return response(200, "Berhasil", True, currencys_schema.dump(result))
            except ProgrammingError as e:
                print(e)
                return UpdateTable([CurrencyMdb, CurrencyDdb], request)




               