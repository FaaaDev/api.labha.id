import operator
import base64
from datetime import datetime
from itertools import groupby
from ...model.kateg_mdb import KategMdb
from ...model.accou_mdb import AccouMdb
from ...model.transddb import TransDdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy import and_, extract, between
from ...schema.accou_mdb import accou_schema
from ...schema.transddb import trans_schema


class TransFunction:
    date_start = ""
    date_end = ""
    trx_code = ""

    def __new__(self, date_start, date_end, trx_code):
        self.date_start = base64.b64decode(date_start).decode()
        self.date_end = base64.b64decode(date_end).decode()
        self.trx_code = base64.b64decode(trx_code).decode()

        print(self.date_start, self.date_end, self.trx_code)

        if self.trx_code != "0":
            trn = (
                db.session.query(TransDdb, AccouMdb)
                .outerjoin(AccouMdb, TransDdb.acc_id == AccouMdb.id)
                .filter(
                    TransDdb.trx_code == self.trx_code,
                )
                .order_by(TransDdb.trx_dbcr)
                .order_by(TransDdb.trx_date.asc())
                .all()
            )
        else:
            
            trn = (
                db.session.query(TransDdb, AccouMdb)
                .outerjoin(AccouMdb, TransDdb.acc_id == AccouMdb.id)
                .filter(
                    TransDdb.trx_date.between(
                        datetime.strptime(self.date_start, "%d/%m/%Y"),
                        datetime.strptime(self.date_end, "%d/%m/%Y").replace(
                            hour=23, minute=59, second=59
                        ),
                    )
                )
                .order_by(TransDdb.trx_dbcr)
                .order_by(TransDdb.trx_date.asc())
                .all()
            )
            

        header = []

        get_attr = operator.attrgetter("trx_code")

        for k, g in groupby(sorted([x[0] for x in trn], key=get_attr), key=get_attr):
            trx_date = ""
            for x in g:
                trx_date = x.trx_date.strftime("%d/%m/%Y")
            header.append(
                {
                    "trx_code": k,
                    "trx_date": trx_date,
                    "trx": [],
                }
            )

        for x in header:
            for y in trn:
                if x["trx_code"] == y[0].trx_code:
                    x["trx"].append(
                        {
                            "acc_id": {
                                "acc_code": y[1].acc_code,
                                "acc_name": y[1].acc_name,
                            },
                            "trx_date": y[0].trx_date.isoformat(),
                            "trx_dbcr": y[0].trx_dbcr,
                            "trx_amnt": y[0].trx_amnt,
                            "trx_desc": y[0].trx_desc,
                        }
                    )

        return response(
            200,
            "Berhasil",
            True,
            header,
        )
