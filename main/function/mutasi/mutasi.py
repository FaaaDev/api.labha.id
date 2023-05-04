from main.function.update_mutasi import UpdateMutasi
from main.function.update_table import UpdateTable
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.mtsi_hdb import MtsiHdb
from main.model.prod_mdb import ProdMdb
from main.model.proj_mdb import ProjMdb
from main.model.unit_mdb import UnitMdb
from main.model.mtsi_ddb import MtsiDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.mtsi_hdb import MtsiSchema, mtsi_schema
from main.schema.mtsi_ddb import mtsiddb_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.proj_mdb import proj_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.ccost_mdb import ccost_schema


class Mutasi:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                mtsi_code = request.json["mtsi_code"]
                mtsi_date = request.json["mtsi_date"]
                loc_from = request.json["loc_from"]
                loc_to = request.json["loc_to"]
                dep_id = request.json["dep_id"]
                prj_id = request.json["prj_id"]
                doc = request.json["doc"]
                doc_date = request.json["doc_date"]
                approve = request.json["approve"]
                desc = request.json["desc"]
                mutasi = request.json["mutasi"]

                mt = MtsiHdb(
                    mtsi_code,
                    mtsi_date,
                    loc_from,
                    loc_to,
                    dep_id,
                    prj_id,
                    doc,
                    doc_date,
                    desc,
                    False,
                )

                db.session.add(mt)
                db.session.commit()

                new_mutasi = []
                for x in mutasi:
                    if x["prod_id"] and x["qty"] and x["unit_id"]:
                        new_mutasi.append(
                            MtsiDdb(
                                mt.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["qty"],
                                x["qty_terima"],
                            )
                        )

                if len(new_mutasi) > 0:
                    db.session.add_all(new_mutasi)
                    db.session.commit()
                # UpdateMutasi(mt.id, False)

            except IntegrityError as e:
                print(e)
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, mtsi_schema.dump(mt))
        else:
            try:
                mt = (
                    db.session.query(MtsiHdb, CcostMdb, ProjMdb)
                    .outerjoin(CcostMdb, CcostMdb.id == MtsiHdb.dep_id)
                    .outerjoin(ProjMdb, ProjMdb.id == MtsiHdb.prj_id)
                    .order_by(MtsiHdb.id.desc())
                    .all()
                )

                mts = (
                    db.session.query(MtsiDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == MtsiDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == MtsiDdb.unit_id)
                    .all()
                )

                loc = LocationMdb.query.all()

                final = []
                for x in mt:
                    mut = []
                    for y in mts:
                        if x[0].id == y[0].mtsi_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            mut.append(mtsiddb_schema.dump(y[0]))

                    for y in loc:
                        if x[0].loc_from == y.id:
                            x[0].loc_from = loct_schema.dump(y)

                        if x[0].loc_to == y.id:
                            x[0].loc_to = loct_schema.dump(y)

                    final.append(
                        {
                            "id": x[0].id,
                            "mtsi_code": x[0].mtsi_code,
                            "mtsi_date": MtsiSchema(only=["mtsi_date"]).dump(x[0])[
                                "mtsi_date"
                            ],
                            "loc_from": x[0].loc_from,
                            "loc_to": x[0].loc_to,
                            "dep_id": ccost_schema.dump(x[1]) if x[1] else None,
                            "prj_id": proj_schema.dump(x[2]) if x[2] else None,
                            "doc": x[0].doc,
                            "doc_date": MtsiSchema(only=["doc_date"]).dump(x[0])[
                                "doc_date"
                            ],
                            "desc": x[0].desc,
                            "approve": x[0].approve,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "mutasi": mut,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [MtsiHdb, CcostMdb, ProjMdb, MtsiDdb, ProdMdb, UnitMdb], request
                )
