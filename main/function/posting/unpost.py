from datetime import date, datetime
from math import prod
from main.model.comp_mdb import CompMdb
from main.model.accou_ddb import AccouDdb
from main.model.transddb import TransDdb
from main.model.setup_mdb import SetupMdb
from main.model.user import User
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError


class Unpost:
    def __new__(self, user, month, year, request):
        ddb = AccouDdb.query.filter(
            and_(
                AccouDdb.acc_month == month,
                AccouDdb.acc_year == year,
                AccouDdb.from_closing == False,
            )
        ).all()

        trn = TransDdb.query.filter(
            and_(
                TransDdb.gen_post == True,
                extract("month", TransDdb.trx_date) == month,
                extract("year", TransDdb.trx_date) == year,
            )
        ).all()

        for x in ddb:
            db.session.delete(x)

        for x in trn:
            x.gen_post = False
            x.post_date = None

        db.session.commit()

        return response(200, "Berhasil", True, None)
