from main.function.update_table import UpdateTable
from main.function.update_memorial import UpdateMemorial
from ...model.accou_mdb import AccouMdb
from ...schema.accou_mdb import accou_schema
from ...model.memo_hdb import MemoHdb
from ...schema.memo_hdb import MhdbSchema, mhdb_schema
from ...model.ccost_mdb import CcostMdb
from ...schema.ccost_mdb import ccost_schema
from ...model.memo_ddb import MemoDdb
from ...schema.memo_ddb import mddb_schema
from ...model.bank_mdb import BankMdb
from ...schema.bank_mdb import bank_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...model.currency_mdb import CurrencyMdb
from ...schema.currency_mdb import currency_schema
from ...model.transddb import TransDdb
from ...model.transbank import TransBank


class Memorial:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                desc = request.json["desc"]
                memo = request.json["memo"]

                m = MemoHdb(code, date, desc, False, user.id)

                db.session.add(m)
                db.session.commit()

                new_memo = []
                for x in memo:
                    if x["dbcr"] and x["amnt"]:
                        new_memo.append(
                            MemoDdb(
                                m.id,
                                x["acc_id"],
                                x["bank_id"],
                                x["dep_id"],
                                x["currency"],
                                x["dbcr"],
                                x["amnt"],
                                x["amnh"],
                                x["desc"],
                                user.id,
                            )
                        )

                    # print(len(new_memo))
                if len(new_memo) > 0:
                    db.session.add_all(new_memo)
                    db.session.commit()

                UpdateMemorial(m.id, False, user.id)

                print(new_memo)

            except Exception as e:
                print(e)
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, mhdb_schema.dump(m))
        else:
            try:
                m = (
                    MemoHdb.query.filter(MemoHdb.closing == False)
                    .order_by(MemoHdb.id.desc())
                    .all()
                )

                memo = (
                    db.session.query(MemoDdb, AccouMdb, CcostMdb, CurrencyMdb, BankMdb)
                    .outerjoin(AccouMdb, AccouMdb.id == MemoDdb.acc_id)
                    .outerjoin(CcostMdb, CcostMdb.id == MemoDdb.dep_id)
                    .outerjoin(CurrencyMdb, CurrencyMdb.id == MemoDdb.currency)
                    .outerjoin(BankMdb, BankMdb.id == MemoDdb.bank_id)
                    .all()
                )

                final = []
                for x in m:
                    mm = []
                    for y in memo:
                        if x.id == y[0].mcode:
                            y[0].acc_id = accou_schema.dump(y[1])
                            y[0].dep_id = ccost_schema.dump(y[2])
                            y[0].currency = currency_schema.dump(y[3]) if y[3] else None
                            y[0].bank_id = bank_schema.dump(y[4]) if y[4] else None
                            mm.append(mddb_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x.id,
                            "code": x.code,
                            "date": MhdbSchema(only=["date"]).dump(x)["date"],
                            "desc": x.desc,
                            "imp": x.imp,
                            "memo": mm,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [MemoHdb, MemoDdb, AccouMdb, CcostMdb, CurrencyMdb], request
                )
