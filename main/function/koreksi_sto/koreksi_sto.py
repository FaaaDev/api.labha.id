from ...function.update_table import UpdateTable
from ...function.update_koreksi_sto import UpdateKoreksiSto
from ...model.koreksi_sto_hdb import KorStoHdb
from ...model.koreksi_sto_ddb import KorStoDdb
from ...model.ccost_mdb import CcostMdb
from ...model.prod_mdb import ProdMdb
from ...model.proj_mdb import ProjMdb
from ...model.unit_mdb import UnitMdb
from ...model.lokasi_mdb import LocationMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.koreksi_sto_hdb import KorStoSchema, korSto_schema
from ...schema.koreksi_sto_ddb import korStoddb_schema
from ...schema.ccost_mdb import ccost_schema
from ...schema.proj_mdb import proj_schema
from ...schema.prod_mdb import prod_schema
from ...schema.unit_mdb import unit_schema
from ...schema.lokasi_mdb import loct_schema


class KoreksiPersediaan:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                dep_id = request.json["dep_id"]
                proj_id = request.json["proj_id"]
                kprod = request.json["kprod"]
                kor = KorStoHdb(code, date, dep_id, proj_id, user.id)

                db.session.add(kor)
                db.session.commit()

                new_product = []
                for x in kprod:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        new_product.append(
                            KorStoDdb(
                                kor.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["location"],
                                x["dbcr"],
                                x["qty"],
                            )
                        )

                if len(new_product) > 0:
                    db.session.add_all(new_product)
                    db.session.commit()

                UpdateKoreksiSto(kor.id, False)

            except IntegrityError:
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, korSto_schema.dump(kor))
        else:
            try:
                kor = (
                    db.session.query(KorStoHdb, CcostMdb, ProjMdb)
                    .outerjoin(CcostMdb, CcostMdb.id == KorStoHdb.dep_id)
                    .outerjoin(ProjMdb, ProjMdb.id == KorStoHdb.proj_id)
                    .order_by(KorStoHdb.id.desc())
                    .all()
                )

                kprod = (
                    db.session.query(KorStoDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == KorStoDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == KorStoDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == KorStoDdb.location)
                    .all()
                )

                final = []
                for x in kor:
                    prod = []
                    for y in kprod:
                        if y[0].kor_id == x[0].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].location = loct_schema.dump(y[3])
                            prod.append(korStoddb_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": KorStoSchema(only=["date"]).dump(x[0])["date"],
                            "dep_id": ccost_schema.dump(x[1]) if x[1] else None,
                            "proj_id": proj_schema.dump(x[2]) if x[2] else None,
                            "kprod": prod,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        KorStoHdb,
                        CcostMdb,
                        ProjMdb,
                        KorStoDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                    ],
                    request,
                )
