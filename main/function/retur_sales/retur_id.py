from main.model.ordpj_hdb import OrdpjHdb
from main.model.prod_mdb import ProdMdb
from main.model.reprod_ddb import ReprodDdb
from main.model.retsale_hdb import RetSaleHdb
from main.model.sord_hdb import SordHdb
from main.model.unit_mdb import UnitMdb
from main.schema.retsale_hdb import RetSaleSchema, retsale_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.reprod_ddb import reprod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.ordpj_hdb import ordpj_schema
from main.schema.sord_hdb import sord_schema


class ReturSaleId:
    def __new__(self, id, request):
        ret = RetSaleHdb.query.filter(RetSaleHdb.id == id).first()
        if request.method == "PUT":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                sale_id = request.json["sale_id"]
                product = request.json["product"]

                ret.ret_code = ret_code
                ret.ret_date = ret_date
                ret.sale_id = sale_id

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

                result = response(200, "Berhasil", True, retsale_schema.dump(ret))

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
                db.session.query(RetSaleHdb, OrdpjHdb, SordHdb)
                .outerjoin(OrdpjHdb, OrdpjHdb.id == RetSaleHdb.sale_id)
                .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
                .filter(RetSaleHdb.id == id)
                .first()
            )

            product = (
                db.session.query(ReprodDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
                .all()
            )

            product = []
            for y in product:
                if y[0].id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(reprod_schema.dump(y[0]))

            final = {
                "id": x[0].id,
                "ret_code": x[0].ret_code,
                "ret_date": RetSaleSchema(only=["ret_date"]).dump(x[0])["ret_date"],
                "sale_id": ordpj_schema.dump(x[2]) if x[2] else None,
                "product": product,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
