from main.function.update_koreksi_sto import UpdateKoreksiSto
from main.model.koreksi_sto_hdb import KorStoHdb
from main.model.koreksi_sto_ddb import KorStoDdb
from main.model.ccost_mdb import CcostMdb
from main.model.prod_mdb import ProdMdb
from main.model.proj_mdb import ProjMdb
from main.model.unit_mdb import UnitMdb
from main.model.lokasi_mdb import LocationMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.koreksi_sto_hdb import KorStoSchema, korSto_schema
from main.schema.koreksi_sto_ddb import korStoddb_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.proj_mdb import proj_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.lokasi_mdb import loct_schema


class KorPersediaanId:
    def __new__(self, id, request):
        kor = KorStoHdb.query.filter(KorStoHdb.id == id).first()
        if request.method == "PUT":
            try:
                code = request.json["code"]
                date = request.json["date"]
                dep_id = request.json["dep_id"]
                proj_id = request.json["proj_id"]
                kprod = request.json["kprod"]

                kor.code = code
                kor.date = date
                kor.dep_id = dep_id
                kor.proj_id = proj_id

                db.session.commit()

                old_koreksi = KorStoDdb.query.filter(KorStoDdb.kor_id == id).all()
                new_koreksi = []
                for z in kprod:
                    if z["id"]:
                        for y in old_koreksi:
                            if z["id"] == y.id:
                                if z["id"] and z["prod_id"] and z["qty"] and z["unit_id"]:
                                    y.prod_id = z["prod_id"]
                                    y.unit_id = z["unit_id"]
                                    y.location = z["location"]
                                    y.dbcr = z["dbcr"]
                                    y.qty = z["qty"]
                    else:
                        if z["prod_id"] and z["qty"] and z["unit_id"]:
                            new_koreksi.append(
                                KorStoDdb(
                                    kor.id,
                                    z["prod_id"],
                                    z["unit_id"],
                                    z["location"],
                                    z["dbcr"],
                                    z["qty"],
                                )
                            )

                if len(new_koreksi) > 0:
                    db.session.add_all(new_koreksi)

                db.session.commit()

                UpdateKoreksiSto(kor.id, False)

                result = response(200, "Berhasil", True, korSto_schema.dump(kor))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            UpdateKoreksiSto(kor.id, True)
            old_koreksi = KorStoDdb.query.filter(KorStoDdb.kor_id == id).all()
            if old_koreksi:
                for y in old_koreksi:
                    db.session.delete(y)

            db.session.delete(kor)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)

        return self.response
