from ...model.koreksi_piutang_hdb import KorPiutangHdb
from ...model.arcard_mdb import ArCard
from ...model.transddb import TransDdb
from ...model.currency_mdb import CurrencyMdb
from ...model.custom_mdb import CustomerMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.koreksi_piutang_hdb import KoreksiPiuSchema, korPiut_schema
from ...schema.custom_mdb import customer_schema


class KoreksiPiutangId:
    def __new__(self, id, request):
        kor_piutang = KorPiutangHdb.query.filter(KorPiutangHdb.id == id).first()
        if request.method == "PUT":
            try:
                kor_piutang.code = request.json["code"]
                kor_piutang.date = request.json["date"]
                kor_piutang.cus_id = request.json["cus_id"]
                kor_piutang.type_kor = request.json["type_kor"]
                kor_piutang.value = request.json["value"]
                kor_piutang.due_date = request.json["due_date"]
                kor_piutang.desc = request.json["desc"]
                db.session.commit()

                cus = CustomerMdb.query.filter(
                    CustomerMdb.id == kor_piutang.cus_id
                ).first()

                curr = CurrencyMdb.query.all()

                cur_rate = 0
                for x in curr:
                    if x.id == cus.cus_curren:
                        cur_rate = x.rate

                old_ar = ArCard.query.filter(
                    ArCard.trx_code == kor_piutang.code and ArCard.trx_type == "KOR"
                ).all()

                if old_ar:
                    for x in old_ar:
                        db.session.delete(x)

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

                # Create Jurnal Koreksi Piutang
                old_trn = TransDdb.query.filter(
                    TransDdb.trx_code == kor_piutang.code
                ).all()

                if old_trn:
                    for x in old_trn:
                        db.session.delete(x)

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
                    "JURNAL KOREKSI HUTANG ATAS CUSTOMER %s" % (cus.cus_code),
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
                    "JURNAL KOREKSI HUTANG ATAS CUSTOMER %s" % (cus.cus_code),
                    None,
                    None,
                )

                db.session.add(new_trans_kor)
                db.session.commit()

                result = response(
                    200, "Berhasil", True, korPiut_schema.dump(kor_piutang)
                )
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        elif request.method == "DELETE":
            old_trn = TransDdb.query.filter(TransDdb.trx_code == kor_piutang.code).all()
            if old_trn:
                for x in old_trn:
                    db.session.delete(x)

            old_ar = ArCard.query.filter(
                ArCard.trx_code == kor_piutang.code and ArCard.trx_type == "KOR"
            ).all()
            if old_ar:
                for x in old_ar:
                    db.session.delete(x)

            db.session.delete(kor_piutang)
            db.session.commit()
            self.response = response(200, "Berhasil", True, None)
        else:
            self.response = response(
                200, "Berhasil", True, korPiut_schema.dump(kor_piutang)
            )

        return self.response
