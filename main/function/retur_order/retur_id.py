from ...function.update_retur_beli import UpdateReturOrd
from ...model.fkpb_hdb import FkpbHdb
from ...model.stcard_mdb import StCard
from ...model.lokasi_mdb import LocationMdb
from ...model.ordpb_hdb import OrdpbHdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.reprod_ddb import ReprodDdb
from ...model.retord_hdb import RetordHdb
from ...model.unit_mdb import UnitMdb
from ...schema.dord_hdb import DordSchema, dord_schema
from ...schema.retord_hdb import RetordSchema, retord_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.prod_mdb import prod_schema
from ...schema.reprod_ddb import reprod_schema
from ...schema.unit_mdb import unit_schema
from ...schema.lokasi_mdb import loct_schema
from ...schema.fkpb_hdb import FkpbSchema, fkpb_schema


class ReturOrderId:
    def __new__(self, id, request):
        ret = RetordHdb.query.filter(RetordHdb.id == id).first()
        if request.method == "PUT":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                fk_id = request.json["fk_id"]
                inv_id = request.json["inv_id"]
                product = request.json["product"]

                ret.ret_code = ret_code
                ret.ret_date = ret_date
                ret.fk_id = None
                ret.inv_id = inv_id

                o_product = ReprodDdb.query.filter(ReprodDdb.id == id).all()

                old_prod = []
                new_prod = []
                for x in product:
                    if x["id"]:
                        if x["prod_id"] and x["unit_id"] and x["retur"]:
                            old_prod.append(x["id"])

                    else:
                        if x["prod_id"] and x["unit_id"] and x["retur"]:
                            new_prod.append(
                                ReprodDdb(
                                    ret.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["retur"],
                                    x["price"],
                                    x["disc"],
                                    x["nett_price"],
                                    x["totl"],
                                    x["totl_fc"],
                                    x["location"],
                                )
                            )

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in o_product:
                            if y.id not in old_prod:
                                db.session.delete(y)

                            else:
                                if y.id == x:
                                    for z in product:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.retur = z["retur"]
                                            y.price = z["price"]
                                            y.disc = z["disc"]
                                            y.nett_price = z["nett_price"]
                                            y.totl = z["totl"]
                                            y.totl_fc = z["totl_fc"]
                                            y.location = z["location"]

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                db.session.commit()

                UpdateReturOrd(ret.id, id, False)

                result = response(200, "Berhasil", True, retord_schema.dump(ret))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            UpdateReturOrd(ret.id, id, True)

            old_prod = ReprodDdb.query.filter(ReprodDdb.ret_id == ret.id).all()
            if old_prod:
                for x in old_prod:
                    db.session.delete(x)
                    db.session.commit()
                    
            db.session.delete(ret)
            db.session.commit()

            self.response = response(200, "success", True, None)

        else:
            x = (
                db.session.query(RetordHdb, FkpbHdb, OrdpbHdb)
                .outerjoin(FkpbHdb, FkpbHdb.id == RetordHdb.fk_id)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
                .filter(RetordHdb.id == id)
                .first()
            )

            product = (
                db.session.query(ReprodDdb, ProdMdb, UnitMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
                .outerjoin(LocationMdb, LocationMdb.id == ReprodDdb.location)
                .all()
            )

            product = []
            for y in product:
                if y[0].id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    y[0].location = loct_schema.dump(y[2])
                    product.append(reprod_schema.dump(y[0]))

            final = {
                "id": x[0].id,
                "ret_code": x[0].ret_code,
                "ret_date": RetordSchema(only=["ret_date"]).dump(x[0])["ret_date"],
                "fk_id": fkpb_schema.dump(x[2]) if x[2] else None,
                "product": product,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
