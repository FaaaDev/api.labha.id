from main.function.update_table import UpdateTable
from main.function.write_activity import WriteActivity
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.usage_material_hdb import UsageMatHdb
from main.model.usage_material_ddb import UsageMatDdb
from main.model.usage_material_biaya_ddb import UsageMatBiayaDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.usage_material_hdb import usage_mat_schema, UsageMatSchema
from main.schema.usage_material_ddb import material_schema
from main.schema.usage_material_biaya_ddb import mat_biaya_schema
from main.schema.ccost_mdb import ccost_schema, ccosts_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class UsageMaterial:
    # response = response(400, "Gagal", True, None)

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                dep_id = request.json["dep_id"]
                loc_id = request.json["loc_id"]
                material = request.json["material"]
                biaya = request.json["biaya"]

                usage = UsageMatHdb(code, date, dep_id, loc_id, user.id)

                db.session.add(usage)
                db.session.commit()

                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                        new_material.append(
                            UsageMatDdb(
                                usage.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["qty"],
                            )
                        )

                new_biaya = []
                for x in biaya:
                    if x["acc_id"]:
                        new_biaya.append(
                            UsageMatBiayaDdb(
                                usage.id,
                                x["acc_id"],
                                x["value"],
                                x["desc"],
                            )
                        )

                if len(new_material) > 0:
                    db.session.add_all(new_material)

                if len(new_biaya) > 0:
                    db.session.add_all(new_biaya)

                WriteActivity(user, code, "TRANSACTION", "ADDED")
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, usage_mat_schema.dump(usage))
        else:
            try:
                usage = (
                    db.session.query(UsageMatHdb, CcostMdb, LocationMdb)
                    .outerjoin(CcostMdb, CcostMdb.id == UsageMatHdb.dep_id)
                    .outerjoin(LocationMdb, LocationMdb.id == UsageMatHdb.loc_id)
                    .order_by(UsageMatHdb.id.desc())
                    .all()
                )

                material = (
                    db.session.query(UsageMatDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == UsageMatDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == UsageMatDdb.unit_id)
                    .all()
                )

                biaya = db.session.query(UsageMatBiayaDdb).all()

                final = []
                for x in usage:

                    mat = []
                    for y in material:
                        if x[0].id == y[0].um_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            mat.append(material_schema.dump(y[0]))

                    cost = []
                    for y in biaya:
                        if x[0].id == y.um_id:
                            cost.append(mat_biaya_schema.dump(y))

                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": UsageMatSchema(only=["date"]).dump(x[0])["date"],
                            "dep_id": ccost_schema.dump(x[1]),
                            "loc_id": loct_schema.dump(x[2]),
                            "user_id": x[0].user_id,
                            "material": mat,
                            "biaya": cost,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                return UpdateTable(
                    [
                        UsageMatHdb,
                        CcostMdb,
                        LocationMdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        UsageMatDdb,
                        UsageMatBiayaDdb,
                    ],
                    request,
                )
