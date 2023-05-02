from datetime import date, datetime
from ...model.comp_mdb import CompMdb
from ...model.akhir_mdb import AkhirMdb
from ...model.accou_ddb import AccouDdb
from ...model.accou_mdb import AccouMdb
from ...model.kateg_mdb import KategMdb
from ...model.setup_mdb import SetupMdb
from ...model.pnl_mdb import PnlMdb
from ...model.transddb import TransDdb
from ...model.user import User
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError


class Closing:
    def __new__(self, user, month, year, request):

        closing = AkhirMdb(month, year, user.id, user.id)

        ddb = (
            db.session.query(AccouDdb, AccouMdb, KategMdb)
            .outerjoin(AccouMdb, AccouDdb.acc_code == AccouMdb.acc_code)
            .outerjoin(KategMdb, KategMdb.id == AccouMdb.kat_code)
            .filter(and_(AccouDdb.acc_month == month, AccouDdb.acc_year == year))
            .all()
        )

        setup_acc = SetupMdb.query.filter(SetupMdb.cp_id == user.company).first()

        setup = PnlMdb.query.filter(PnlMdb.cp_id == user.company).first()
        if setup:
            setup.klasi = (
                setup.klasi.replace("{", "").replace("}", "").split(",")
                if setup.klasi
                else None
            )

            if setup.klasi:
                setup.klasi = [int(x) for x in setup.klasi]

        new_ddb = []
        last_month = 0
        acc_code = ""
        for x in ddb:
            if x[1].id != setup_acc.pnl_year:
                if x[1].id == setup_acc.pnl:
                    last_month = x[0].acc_akhir

                if x[2].kode_klasi in setup.klasi:
                    new_ddb.append(
                        AccouDdb(
                            year + 1 if month == 12 else year,
                            month + 1 if month < 12 else 1,
                            x[0].acc_code,
                            0,
                            0,
                            0,
                            0,
                            False,
                            True,
                            False,
                            user.id,
                        )
                    )
                else:
                    new_ddb.append(
                        AccouDdb(
                            year + 1 if month == 12 else year,
                            month + 1 if month < 12 else 1,
                            x[0].acc_code,
                            0 if x[1].id == setup_acc.pnl else x[0].acc_akhir,
                            0,
                            0,
                            0,
                            False,
                            True,
                            False,
                            user.id,
                        )
                    )
            else:
                acc_code = x[0].acc_code

        new_ddb.append(
            AccouDdb(
                year + 1 if month == 12 else year,
                month + 1 if month < 12 else 1,
                acc_code,
                last_month,
                0,
                0,
                0,
                False,
                True,
                False,
                user.id,
            )
        )

        # trn = (
        #     db.session.query(TransDdb, KbksHdb, MemoHdb)
        #     .outerjoin(KbksHdb, TransDdb.trx_code == KbksHdb.code)
        #     .outerjoin(MemoHdb, TransDdb.trx_code == MemoHdb.code)
        #     .filter(
        #         and_(
        #             TransDdb.gen_post == True,
        #             extract("month", TransDdb.trx_date) == month,
        #             extract("year", TransDdb.trx_date) == year,
        #         )
        #     )
        #     .all()
        # )

        # for x in trn:
        #     if x[1]:
        #         x[1].closing = True
        #     if x[2]:
        #         x[2].closing = True

        db.session.add_all(new_ddb)
        db.session.add(closing)
        db.session.commit()

        return response(200, "Berhasil", True, None)
