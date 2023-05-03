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
from sqlalchemy.exc import IntegrityError
from main.schema.usage_material_hdb import usage_mat_schema, UsageMatSchema
from main.schema.usage_material_ddb import material_schema
from main.schema.usage_material_biaya_ddb import mat_biaya_schema
from main.schema.ccost_mdb import ccost_schema, ccosts_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class UsageMaterialId:
    def __new__(self, user, id, request):
        usage = UsageMatHdb.query.filter(UsageMatHdb.id == id).first()
        if request.method == "PUT":
            try:
                code = request.json["code"]
                date = request.json["date"]
                dep_id = request.json["dep_id"]
                loc_id = request.json["loc_id"]
                material = request.json["material"]
                biaya = request.json["biaya"]

                usage.code = code
                usage.date = date
                usage.dep_id = dep_id
                usage.loc_id = loc_id

                mat = UsageMatDdb.query.filter(UsageMatDdb.um_id == usage.id).all()
                cost = UsageMatBiayaDdb.query.filter(
                    UsageMatBiayaDdb.um_id == usage.id
                ).all()

                old_mat = []
                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_mat.append(x["id"])
                        else:
                            new_material.append(
                                UsageMatDdb(
                                    usage.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["qty"],
                                )
                            )

                if len(old_mat) > 0:
                    for x in old_mat:
                        for y in mat:
                            if y.id not in old_mat:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in material:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.qty = z["qty"]

                old_biaya = []
                new_biaya = []
                for x in biaya:
                    if x["acc_id"]:
                        if x["id"] != 0:
                            old_biaya.append(x["id"])
                        else:
                            new_biaya.append(
                                UsageMatBiayaDdb(
                                    usage.id,
                                    x["acc_id"],
                                    x["value"],
                                    x["desc"],
                                )
                            )

                if len(old_biaya) > 0:
                    for x in old_biaya:
                        for y in cost:
                            if y.id not in old_biaya:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in biaya:
                                        if z["id"] == x:
                                            y.acc_id = z["acc_id"]
                                            y.value = z["value"]
                                            y.desc = z["desc"]

                if len(new_material) > 0:
                    db.session.add_all(new_material)

                if len(new_biaya) > 0:
                    db.session.add_all(new_biaya)

                WriteActivity(user, code, "TRANSACTION", "EDITED")
                db.session.commit()

                result = response(200, "Berhasil", True, usage_mat_schema.dump(usage))

            except Exception as e:
                print(e)
                db.session.rollback()
                result = response(
                    400, "Tidak dapat mengedit data karena status", False, None
                )
            finally:
                self.response = result

        elif request.method == "DELETE":
            code = usage.code
            WriteActivity(user, code, "TRANSACTION", "DELETED")

            material = UsageMatDdb.query.filter(UsageMatDdb.um_id == id).all()
            cost = UsageMatBiayaDdb.query.filter(
                UsageMatBiayaDdb.um_id == id
            ).all()

            if material:
                for x in material:
                    db.session.delete(x)

            if cost:
                for x in cost:
                    db.session.delete(x)

            db.session.delete(usage)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
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

            self.response = response(200, "Berhasil", True, final)

        return self.response
