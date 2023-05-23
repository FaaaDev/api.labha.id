from main.function.update_table import UpdateTable
from ...model.accou_mdb import AccouMdb
from ...schema.accou_mdb import accou_schema
from ...model.memo_hdb import MemoHdb
from ...schema.memo_hdb import MhdbSchema, mhdb_schema
from ...model.ccost_mdb import CcostMdb
from ...schema.ccost_mdb import ccost_schema
from ...model.memo_ddb import MemoDdb
from ...schema.memo_ddb import mddb_schema
from ...shared.shared import db
from ...utils.response import response
from ...model.currency_mdb import CurrencyMdb
from ...schema.currency_mdb import currency_schema
from sqlalchemy import func, cast, case, literal_column, or_
from sqlalchemy.exc import *


class MemorialFilter:
    def __new__(self, page, length, filter, request):
        try:
            all = (
                MemoHdb.query.filter(MemoHdb.closing == False)
                .filter(
                    or_(
                        func.lower(MemoHdb.code).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                        func.lower(MemoHdb.desc).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                    )
                )
                .all()
            )

            m = (
                MemoHdb.query.filter(MemoHdb.closing == False)
                .filter(
                    or_(
                        func.lower(MemoHdb.code).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                        func.lower(MemoHdb.desc).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                    )
                )
                .order_by(MemoHdb.id.desc())
                .offset(length * (page - 1))
                .limit(length)
                .all()
            )

            memo = (
                db.session.query(MemoDdb, AccouMdb, CcostMdb, CurrencyMdb)
                .outerjoin(AccouMdb, AccouMdb.id == MemoDdb.acc_id)
                .outerjoin(CcostMdb, CcostMdb.id == MemoDdb.dep_id)
                .outerjoin(CurrencyMdb, CurrencyMdb.id == MemoDdb.currency)
                .filter(MemoDdb.mcode.in_(tuple([x.id for x in m])))
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

            return response(200, "Berhasil", True, {"data": final, "length": len(all)})

        except ProgrammingError as e:
            return UpdateTable(
                [MemoHdb, MemoDdb, AccouMdb, CcostMdb, CurrencyMdb], request
            )
