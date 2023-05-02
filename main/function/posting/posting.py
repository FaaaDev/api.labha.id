from datetime import date, datetime
from ...model.comp_mdb import CompMdb
from ...model.accou_ddb import AccouDdb
from ...model.accou_mdb import AccouMdb
from ...model.kateg_mdb import KategMdb
from ...model.setup_mdb import SetupMdb
from ...model.pnl_mdb import PnlMdb
from ...model.transddb import TransDdb
from ...model.user import User
from ...schema.accou_ddb import AccddbSchema, accddb_schema, accddbs_schema
from ...schema.accou_mdb import AccouSchema, accou_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError


class Posting:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                post_year = request.json["post_year"]
                post_month = request.json["post_month"]

                acc = AccouMdb.query.filter(AccouMdb.dou_type == "D").all()

                trn = (
                    db.session.query(TransDdb, AccouMdb, KategMdb)
                    .outerjoin(AccouMdb, TransDdb.acc_id == AccouMdb.id)
                    .outerjoin(KategMdb, KategMdb.id == AccouMdb.kat_code)
                    .filter(
                        and_(
                            extract("month", TransDdb.trx_date) == post_month,
                            extract("year", TransDdb.trx_date) == post_year,
                        )
                    )
                    .all()
                )

                old = (
                    AccouDdb.query.filter(AccouDdb.sa == True)
                    .order_by(AccouDdb.id.asc())
                    .all()
                )

                closing = (
                    AccouDdb.query.filter(
                        and_(
                            AccouDdb.acc_month == post_month,
                            AccouDdb.acc_year == post_year,
                            AccouDdb.from_closing == True,
                        )
                    )
                    .order_by(AccouDdb.id.asc())
                    .all()
                )

                other = (
                    AccouDdb.query.filter(
                        and_(
                            AccouDdb.acc_month == post_month,
                            AccouDdb.acc_year == post_year,
                            AccouDdb.from_closing == False,
                            AccouDdb.sa == False,
                            AccouDdb.transfer == False,
                        )
                    )
                    .order_by(AccouDdb.id.asc())
                    .all()
                )

                if other:
                    for x in other:
                        db.session.delete(x)
                    db.session.commit()

                setup = PnlMdb.query.filter(PnlMdb.cp_id == user.company).first()
                if setup:
                    setup.klasi = (
                        setup.klasi.replace("{", "").replace("}", "").split(",")
                        if setup.klasi
                        else None
                    )

                transfer = AccouDdb.query.filter(
                    and_(
                        AccouDdb.transfer == True,
                        AccouDdb.acc_month == post_month,
                        AccouDdb.acc_year == post_year,
                    )
                ).all()

                setup_acc = SetupMdb.query.filter(
                    SetupMdb.cp_id == user.company
                ).first()

                new_post = []
                for x in acc:
                    d = 0
                    k = 0
                    sa = 0
                    sales = 0
                    purchase = 0
                    other = 0
                    for y in trn:
                        if y[2].kode_klasi == int(setup.klasi[0]):
                            if y[1].sld_type == "K":
                                sales += y[0].trx_amnt
                            else:
                                sales -= y[0].trx_amnt

                        if y[2].kode_klasi == int(setup.klasi[1]):
                            purchase += y[0].trx_amnt

                        for z in setup.klasi:
                            if z != setup.klasi[0] and z != setup.klasi[1]:
                                if y[2].kode_klasi == int(z):
                                    other += y[0].trx_amnt

                        if x.id == y[0].acc_id:
                            y[0].gen_post = True
                            y[0].post_date = datetime.utcnow()
                            if y[0].trx_dbcr == "D":
                                d += y[0].trx_amnt
                            else:
                                k += y[0].trx_amnt

                    if len(closing) > 0:
                        for z in closing:
                            if x.acc_code == z.acc_code:
                                sa += z.acc_awal
                    else:
                        for z in old:
                            if x.acc_code == z.acc_code:
                                sa += z.acc_awal

                    for y in transfer:
                        if x.acc_code == y.acc_code:
                            d += y.acc_debit
                            k += y.acc_kredit

                    if x.sld_type == "K":
                        akhir = sa - d + k
                    else:
                        akhir = sa + d - k

                    if x.id == setup_acc.pnl:
                        print("====================================================")
                        print(sales - purchase - other)
                        new_post.append(
                            AccouDdb(
                                post_year,
                                post_month,
                                x.acc_code,
                                0,
                                0,
                                0,
                                sales - purchase - other,
                                False,
                                False,
                                False,
                                user.id,
                            )
                        )
                    else:
                        print("====================================================")
                        print(akhir)
                        new_post.append(
                            AccouDdb(
                                post_year,
                                post_month,
                                x.acc_code,
                                0 if len(closing) > 0 else sa,
                                d,
                                k,
                                akhir,
                                False,
                                False,
                                False,
                                user.id,
                            )
                        )

                db.session.add_all(new_post)
                db.session.commit()

                result = response(200, "Berhasil", True, accddbs_schema.dump(new_post))
            except Exception as e:
                db.session.rollback()
                db.session.close()

                print(e)

                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            ddb = (
                db.session.query(AccouDdb, AccouMdb)
                .outerjoin(AccouMdb, AccouMdb.acc_code == AccouDdb.acc_code)
                .order_by(AccouDdb.id.desc())
                .all()
            )

            final = []
            for x in ddb:
                x[0].acc_code = accou_schema.dump(x[1])
                final.append(accddb_schema.dump(x[0]))

            return response(200, "Berhasil", True, final)
