from ...model.accou_mdb import AccouMdb
from main.function.update_memorial import UpdateMemorial
from ...schema.accou_mdb import accou_schema
from ...model.memo_hdb import MemoHdb
from ...schema.memo_hdb import MhdbSchema, mhdb_schema
from ...model.ccost_mdb import CcostMdb
from ...schema.ccost_mdb import ccost_schema
from ...model.memo_ddb import MemoDdb
from ...schema.memo_ddb import mddb_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...model.currency_mdb import CurrencyMdb
from ...schema.currency_mdb import currency_schema
from ...model.transddb import TransDdb
from ...model.transbank import TransBank


class MemorialId:
    def __new__(self, id, request, user_id):
        x = MemoHdb.query.filter(MemoHdb.id == id).first()
        if request.method == "PUT":
            try:
                code = request.json["code"]
                date = request.json["date"]
                desc = request.json["desc"]
                memo = request.json["memo"]

                x.code = code
                x.date = date
                x.desc = desc

                db.session.commit()

                old_memo = MemoDdb.query.filter(MemoDdb.mcode == id).all()
                new_memo = []
                for y in old_memo:
                    for z in memo:
                        if z["id"]:
                            if z["id"] == y.id:
                                if z["id"] and z["dbcr"] and z["amnt"]:
                                    y.acc_id = z["acc_id"]
                                    y.bank_id = z["bank_id"]
                                    y.dep_id = z["dep_id"]
                                    y.currency = z["currency"]
                                    y.dbcr = z["dbcr"]
                                    y.amnt = z["amnt"]
                                    y.amnh = z["amnh"]
                                    y.desc = z["desc"]

                        else:

                            if z["dbcr"] and z["amnt"]:
                                new_memo.append(
                                    MemoDdb(
                                        x.id,
                                        z["acc_id"],
                                        z["bank_id"],
                                        z["dep_id"],
                                        z["currency"],
                                        z["dbcr"],
                                        z["amnt"],
                                        z["amnh"],
                                        z["desc"],
                                        user_id,
                                    )
                                )

                if len(new_memo) > 0:
                    db.session.add_all(new_memo)
                    db.session.commit()

                UpdateMemorial(id, False, user_id)    

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                self.response = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = response(200, "Berhasil", True, mhdb_schema.dump(x))
        elif request.method == "DELETE":
            UpdateMemorial(id, True, user_id)
            
            old_memo = MemoDdb.query.filter(MemoDdb.mcode == id).all()

            if old_memo:
                for y in old_memo:
                    db.session.delete(y)

            db.session.delete(x)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            memo = (
                db.session.query(MemoDdb, AccouMdb, CcostMdb, CurrencyMdb)
                .outerjoin(AccouMdb, AccouMdb.id == MemoDdb.acc_id)
                .outerjoin(CcostMdb, CcostMdb.id == MemoDdb.dep_id)
                .outerjoin(CurrencyMdb, CurrencyMdb.id == MemoDdb.currency)
                .all()
            )

            mm = []
            for y in memo:
                if x.id == y[0].mcode:
                    y[0].acc_id = accou_schema.dump(y[1])
                    y[0].dep_id = ccost_schema.dump(y[2])
                    y[0].currency = currency_schema.dump(y[3]) if y[3] else None
                    mm.append(mddb_schema.dump(y[0]))

            final = {
                "id": x.id,
                "code": x.code,
                "date": MhdbSchema(only=["date"]).dump(x)["date"],
                "desc": x.desc,
                "memo": mm,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
