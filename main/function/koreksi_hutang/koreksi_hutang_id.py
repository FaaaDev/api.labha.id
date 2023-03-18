from main.model.koreksi_hutang_hdb import KorHutangHdb
from main.model.supplier_mdb import SupplierMdb
from main.model.apcard_mdb import ApCard
from main.model.transddb import TransDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.koreksi_hutang_hdb import KoreksiHutSchema, korHut_schema
from main.schema.supplier_mdb import supplier_schema
from main.model.currency_mdb import CurrencyMdb


class KoreksiHutangId:
    def __new__(self, id, request):
        koreksi = KorHutangHdb.query.filter(KorHutangHdb.id == id).first()
        if request.method == "PUT":
            try:
                koreksi.code = request.json["code"]
                koreksi.date = request.json["date"]
                koreksi.sup_id = request.json["sup_id"]
                koreksi.tipe = request.json["tipe"]
                koreksi.acc_lwn = request.json["acc_lwn"]
                koreksi.value = request.json["value"]
                koreksi.due_date = request.json["due_date"]
                koreksi.desc = request.json["desc"]
                db.session.commit()

                sup = SupplierMdb.query.filter(SupplierMdb.id == koreksi.sup_id).first()

                curr = CurrencyMdb.query.all()

                old_ap = ApCard.query.filter(ApCard.trx_code == koreksi.code).all()
                if old_ap:
                    for x in old_ap:
                        db.session.delete(x)

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
                    "d" if koreksi.tipe == "ND" else "k",
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

                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == koreksi.code
                ).all()
                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

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
                    "D" if koreksi.tipe == "ND" else "K",
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
                    koreksi.value * cur_rate
                    if sup.sup_curren != None
                    else koreksi.value,
                    "K" if koreksi.tipe == "ND" else "D",
                    "JURNAL KOREKSI HUTANG ATAS SUPPLIER %s" % (sup.sup_code),
                    None,
                    None,
                )

                db.session.add(new_trans_kor)

                db.session.commit()

                result = response(200, "Berhasil", True, korHut_schema.dump(koreksi))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        elif request.method == "DELETE":
            old_ap = ApCard.query.filter(ApCard.trx_code == koreksi.code).all()
            if old_ap:
                for x in old_ap:
                    db.session.delete(x)

            old_trans = TransDdb.query.filter(TransDdb.trx_code == koreksi.code).all()
            if old_trans:
                for x in old_trans:
                    db.session.delete(x)

            db.session.delete(koreksi)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            self.response = response(200, "Berhasil", True, korHut_schema.dump(koreksi))

        return self.response
