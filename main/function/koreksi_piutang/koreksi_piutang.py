from main.function.update_table import UpdateTable
from main.model.arcard_mdb import ArCard
from main.model.transddb import TransDdb
from main.model.koreksi_piutang_hdb import KorPiutangHdb
from main.model.custom_mdb import CustomerMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.accou_mdb import AccouMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.koreksi_piutang_hdb import KoreksiPiuSchema, korPiut_schema
from main.schema.custom_mdb import customer_schema
from main.schema.accou_mdb import accou_schema


class KoreksiPiutang:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                cus_id = request.json["cus_id"]
                type_kor = request.json["type_kor"]
                acc_lwn = request.json["acc_lwn"]
                value = request.json["value"]
                due_date = request.json["due_date"]
                desc = request.json["desc"]
                kor_piutang = KorPiutangHdb(
                    code,
                    date,
                    cus_id,
                    type_kor,
                    acc_lwn,
                    value,
                    due_date,
                    desc,
                    user.id,
                )
                db.session.add(kor_piutang)
                db.session.commit()

                cus = CustomerMdb.query.filter(
                    CustomerMdb.id == kor_piutang.cus_id
                ).first()

                curr = CurrencyMdb.query.all()

                cur_rate = 0
                for x in curr:
                    if x.id == cus.cus_curren:
                        cur_rate = x.rate

                new_ar = (
                    ArCard(
                        kor_piutang.cus_id,
                        kor_piutang.code,
                        kor_piutang.date,
                        kor_piutang.due_date,
                        None,
                        None,
                        None,
                        None,
                        cus.cus_curren,
                        "D" if kor_piutang.type_kor == "ND" else "K",
                        "KOR",
                        None,
                        kor_piutang.value * cur_rate
                        if cus.cus_curren
                        else kor_piutang.value,
                        kor_piutang.value if cus.cus_curren else 0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        False,
                    ),
                )

                db.session.add(new_ar)

                new_trans_piu = TransDdb(
                    kor_piutang.code,
                    kor_piutang.date,
                    cus.cus_gl,
                    None,
                    None,
                    None,
                    cus.cus_curren,
                    cur_rate if cus.cus_curren != None else None,
                    kor_piutang.value if cus.cus_curren != None else 0,
                    kor_piutang.value * cur_rate
                    if cus.cus_curren != None
                    else kor_piutang.value,
                    "D" if kor_piutang.type_kor == "ND" else "K",
                    "JURNAL KOREKSI PIUTANG ATAS CUSTOMER %s" % (cus.cus_code),
                    None,
                    None,
                )

                db.session.add(new_trans_piu)

                new_trans_kor = TransDdb(
                    kor_piutang.code,
                    kor_piutang.date,
                    kor_piutang.acc_lwn,
                    None,
                    None,
                    None,
                    cus.cus_curren,
                    cur_rate if cus.cus_curren != None else None,
                    kor_piutang.value if cus.cus_curren != None else 0,
                    kor_piutang.value * cur_rate
                    if cus.cus_curren != None
                    else kor_piutang.value,
                    "K" if kor_piutang.type_kor == "ND" else "D",
                    "JURNAL KOREKSI PIUTANG ATAS CUSTOMER %s" % (cus.cus_code),
                    None,
                    None,
                )

                db.session.add(new_trans_kor)
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)

            finally:
                return response(200, "Berhasil", True, korPiut_schema.dump(kor_piutang))
        else:
            try:
                kp = (
                    db.session.query(KorPiutangHdb, CustomerMdb, AccouMdb)
                    .outerjoin(CustomerMdb, CustomerMdb.id == KorPiutangHdb.cus_id)
                    .outerjoin(AccouMdb, AccouMdb.id == KorPiutangHdb.acc_lwn)
                    .order_by(KorPiutangHdb.id.desc())
                    .all()
                )

                final = []
                for x in kp:
                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": KoreksiPiuSchema(only=["date"]).dump(x[0])["date"],
                            "cus_id": customer_schema.dump(x[1]) if x[1] else None,
                            "type_kor": x[0].type_kor,
                            "acc_lwn": accou_schema.dump(x[2]) if x[2] else None,
                            "value": x[0].value,
                            "due_date": KoreksiPiuSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ],
                            "desc": x[0].desc,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable([KorPiutangHdb, CustomerMdb, ArCard], request)
