
from main.function.update_table import UpdateTable
# from main.function.write_activity import WriteActivity
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.fprod_ddb import FprodDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.fprdc_hdb import fprdc_schema, FprdcSchema
from main.schema.fmtrl_ddb import fmtrl_schema
from main.schema.fprod_ddb import fprod_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class Formula:
    # response = response(400, "Gagal", True, None)

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                fcode = request.json["fcode"]
                fname = request.json["fname"]
                version = request.json["version"]
                rev = request.json["rev"]
                desc = request.json["desc"]
                active = request.json["active"]
                date_created = request.json["date_created"]
                product = request.json["product"]
                material = request.json["material"]

                form = FprdcHdb(fcode, fname, version, rev, desc, active, date_created)

                db.session.add(form)
                db.session.commit()

                new_product = []
                for x in product:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                        new_product.append(
                            FprodDdb(
                                form.id, x["prod_id"], x["unit_id"], x["qty"], x["aloc"]
                            )
                        )

                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                        new_material.append(
                            FmtrlDdb(
                                form.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["qty"],
                                x["price"],
                            )
                        )

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                if len(new_material) > 0:
                    db.session.add_all(new_material)

                # WriteActivity(user, fcode, "TRANSACTION", "ADDED")
                # db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, fprdc_schema.dump(form))
        else:
            try:
                form = FprdcHdb.query.order_by(FprdcHdb.id.desc()).all()

                product = (
                    db.session.query(FprodDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
                    .all()
                )

                material = (
                    db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
                    .all()
                )

                final = []
                for x in form:
                    prod = []
                    for y in product:
                        if x.id == y[0].form_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            prod.append(fprod_schema.dump(y[0]))

                    mtrl = []
                    for y in material:
                        if x.id == y[0].form_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            mtrl.append(fmtrl_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x.id,
                            "fcode": x.fcode,
                            "fname": x.fname,
                            "version": x.version,
                            "rev": x.rev,
                            "desc": x.desc,
                            "active": x.active,
                            "date_created": FprdcSchema(only=["date_created"]).dump(x)[
                                "date_created"
                            ],
                            "date_updated": FprdcSchema(only=["date_updated"]).dump(x)[
                                "date_updated"
                            ],
                            "product": prod,
                            "material": mtrl,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                return UpdateTable(
                    [FprdcHdb, FprodDdb, ProdMdb, UnitMdb, FmtrlDdb], request
                )
