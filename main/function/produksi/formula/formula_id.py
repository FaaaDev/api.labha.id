# from main.function.update_dbatch import updateDirectBatch
# from main.function.write_activity import WriteActivity
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.fprod_ddb import FprodDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.fprdc_hdb import fprdc_schema, FprdcSchema
from main.schema.fmtrl_ddb import fmtrl_schema
from main.schema.fprod_ddb import fprod_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class FormulaId:
    def __new__(self, user, id, request):
        fm = FprdcHdb.query.filter(FprdcHdb.id == id).first()
        if request.method == "PUT":
            try:
                fcode = request.json["fcode"]
                fname = request.json["fname"]
                version = request.json["version"]
                rev = request.json["rev"]
                desc = request.json["desc"]
                active = request.json["active"]
                product = request.json["product"]
                material = request.json["material"]

                fm.fcode = fcode
                fm.fname = fname
                fm.version = version
                fm.rev = rev
                fm.desc = desc
                fm.active = active

                db.session.commit()

                prod = FprodDdb.query.filter(FprodDdb.form_id == fm.id).all()
                mat = FmtrlDdb.query.filter(FmtrlDdb.form_id == fm.id).all()

                old_prod = []
                new_product = []
                for x in product:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and x["aloc"]:
                        if x["id"] != 0:
                            old_prod.append(x["id"])
                        else:
                            new_product.append(
                                FprodDdb(
                                    x.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["qty"],
                                    x["aloc"],
                                )
                            )

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in prod:
                            if y.id not in old_prod:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in product:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.qty = z["qty"]
                                            y.aloc = z["aloc"]

                old_mat = []
                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_mat.append(x["id"])
                        else:
                            new_material.append(
                                FmtrlDdb(
                                    x.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["qty"],
                                    x["price"],
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
                                            y.price = z["price"]

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                if len(new_material) > 0:
                    db.session.add_all(new_material)

                # WriteActivity(user, fcode, "TRANSACTION", "EDITED")
                # db.session.commit()

                result = response(200, "Berhasil", True, fprdc_schema.dump(fm))

            except Exception as e:
                print(e)
                db.session.rollback()
                # result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            # fcode = fm.fcode
            # WriteActivity(user, fcode, "TRANSACTION", "DELETED")

            old_prod = FprodDdb.query.filter(FprodDdb.form_id == id).all()
            old_material = FmtrlDdb.query.filter(FmtrlDdb.form_id == id).all()

            for y in old_prod:
                db.session.delete(y)

            for y in old_material:
                db.session.delete(y)

            db.session.delete(fm)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            product = (
                db.session.query(FprodDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
                # .filter(FprodDdb.form_id == id)
                .all()
            )

            material = (
                db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
                # .filter(FprodDdb.form_id == id)
                .all()
            )

            final = []

            for x in fm:
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

                final = {
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

                self.response = response(200, "Berhasil", True, final)

        return self.response
