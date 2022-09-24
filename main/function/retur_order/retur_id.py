from main.model.fkpb_hdb import FkpbHdb
from main.model.stcard_mdb import StCard
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.reprod_ddb import ReprodDdb
from main.model.retord_hdb import RetordHdb
from main.model.unit_mdb import UnitMdb
from main.schema.dord_hdb import DordSchema, dord_schema
from main.schema.retord_hdb import RetordSchema, retord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.reprod_ddb import reprod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.fkpb_hdb import FkpbSchema, fkpb_schema


class ReturOrderId:
    def __new__(self, id, request):
        ret = RetordHdb.query.filter(RetordHdb.id == id).first()
        if request.method == "PUT":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                fk_id = request.json["fk_id"]
                product = request.json["product"]

                ret.ret_code = ret_code
                ret.ret_date = ret_date
                ret.fk_id = fk_id

                # product = ReprodDdb.query.filter(ReprodDdb.id == ret.id)

                new_prod = []
                for x in product:
                    for y in product:
                        if x["id"] == y.id:
                            y.prod_id = x["prod_id"]
                            y.unit_id = x["unit_id"]
                            y.retur = x["retur"]
                            y.price = x["price"]
                            y.disc = x["disc"]
                            y.nett_price = x["nett_price"]
                            y.total = x["total"]
                    if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["retur"]:
                        new_prod.append(
                            ReprodDdb(
                                ret.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["retur"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["total"],
                            )
                        )

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                db.session.commit()


                new_prod = ReprodDdb.query.filter(ReprodDdb.ret_id == id).all()
                old_sto = StCard.query.filter(StCard.trx_code == ret.ret_code).all()
                if old_sto:
                    for y in old_sto:
                        db.session.delete(y)
                        db.session.commit()

                all_sto = []
                for y in new_prod:
                    all_sto.append(
                        StCard(
                            ret.ret_code,
                            ret.ret_date,
                            "k",
                            "RTB",
                            None,
                            y.retur,
                            y.price,
                            y.nett_price if x.nett_price and x.nett_price > 0 else x.totl,
                            None,
                            None,
                            y.disc,
                            y.prod_id,
                            y.location,
                            None,
                            0,
                            None,
                        )
                    )

                if len(all_sto) > 0:
                    db.session.add_all(all_sto)
                    db.session.commit()

                result = response(200, "Berhasil", True, retord_schema.dump(ret))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
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
