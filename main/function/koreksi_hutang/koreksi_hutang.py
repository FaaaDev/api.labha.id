from main.function.update_table import UpdateTable
from main.model.apcard_mdb import ApCard
from main.model.transddb import TransDdb
from main.model.koreksi_hutang_hdb import KorHutangHdb
from main.model.supplier_mdb import SupplierMdb
from main.model.accou_mdb import AccouMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.koreksi_hutang_hdb import KoreksiHutSchema, korHut_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.accou_mdb import accou_schema
from main.model.currency_mdb import CurrencyMdb


class KoreksiHutang:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                sup_id = request.json["sup_id"]
                tipe = request.json["tipe"]
                acc_lwn = request.json["acc_lwn"]
                value = request.json["value"]
                due_date = request.json["due_date"]
                desc = request.json["desc"]
                koreksi = KorHutangHdb(
                    code, date, sup_id, tipe, acc_lwn, value, due_date, desc, user.id
                )
                db.session.add(koreksi)
                db.session.commit()

                sup = SupplierMdb.query.filter(SupplierMdb.id == koreksi.sup_id).first()

                curr = CurrencyMdb.query.all()

                # old_ap = ApCard.query.filter(ApCard.trx_code == koreksi.code).all()
                # if old_ap:
                #     for x in old_ap:
                #         db.session.delete(x)

                new_ap = ApCard(
                    koreksi.code,
                    koreksi.sup_id,
                    None,
                    None,
                    koreksi.date,
                    koreksi.due_date,
                    None,
                    None,
                    None,
                    sup.sup_curren,
                    "d" if tipe == "ND" else "k",
                    "KOR",
                    None,
                    koreksi.value * cur_rate
                    if sup.sup_curren != None
                    else koreksi.value,
                    koreksi.value if sup.sup_curren != None else 0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    False,
                )

                db.session.add(new_ap)

                # Create Jurnal Koreksi Hutang
                cur_rate = 0
                for y in curr:
                    if y.id == sup.sup_curren:
                        cur_rate = y.rate

                new_trans_hut = TransDdb(
                    koreksi.code,
                    koreksi.date,
                    sup.sup_hutang,
                    None,
                    None,
                    None,
                    sup.sup_curren,
                    cur_rate if sup.sup_curren != None else None,
                    koreksi.value if sup.sup_curren != None else 0,
                    koreksi.value * cur_rate
                    if sup.sup_curren != None
                    else koreksi.value,
                    "D" if tipe == "ND" else "K",
                    "JURNAL KOREKSI HUTANG ATAS SUPPLIER %s" % (sup.sup_code),
                    None,
                    None,
                )

                db.session.add(new_trans_hut)

                new_trans_kor = TransDdb(
                    koreksi.code,
                    koreksi.date,
                    koreksi.acc_lwn,
                    None,
                    None,
                    None,
                    sup.sup_curren,
                    cur_rate if sup.sup_curren != None else None,
                    koreksi.value if sup.sup_curren != None else 0,
                    koreksi.value * koreksi.cur_rate
                    if sup.sup_curren != None
                    else koreksi.value,
                    "K" if tipe == "ND" else "D",
                    "JURNAL KOREKSI HUTANG ATAS SUPPLIER %s" % (sup.sup_code),
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
                return response(200, "Berhasil", True, korHut_schema.dump(koreksi))
        else:
            try:
                kh = (
                    db.session.query(KorHutangHdb, SupplierMdb, AccouMdb)
                    .outerjoin(SupplierMdb, SupplierMdb.id == KorHutangHdb.sup_id)
                    .outerjoin(AccouMdb, AccouMdb.id == KorHutangHdb.acc_lwn)
                    .order_by(KorHutangHdb.id.desc())
                    .all()
                )

                final = []
                for x in kh:
                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": KoreksiHutSchema(only=["date"]).dump(x[0])["date"],
                            "sup_id": supplier_schema.dump(x[1]) if x[1] else None,
                            "tipe": x[0].tipe,
                            "acc_lwn": accou_schema.dump(x[2]) if x[2] else None,
                            "value": x[0].value,
                            "due_date": KoreksiHutSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ],
                            "desc": x[0].desc,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [KorHutangHdb, SupplierMdb, ApCard, TransDdb], request
                )
