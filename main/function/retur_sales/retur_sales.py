from main.model.ordpj_hdb import OrdpjHdb
from main.model.prod_mdb import ProdMdb
from main.model.rsprod_ddb import RsprodDdb
from main.model.retsale_hdb import RetSaleHdb
from main.model.sord_hdb import SordHdb
from main.model.stcard_mdb import StCard
from main.model.unit_mdb import UnitMdb
from main.model.lokasi_mdb import LocationMdb
from main.schema.retsale_hdb import RetSaleSchema, retsale_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.rsprod_ddb import rsprod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.ordpj_hdb import ordpj_schema
from main.schema.sord_hdb import sord_schema


class ReturSale:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                sale_id = request.json["sale_id"]
                product = request.json["product"]

                retur = RetSaleHdb(ret_code, ret_date, sale_id)

                db.session.add(retur)
                db.session.commit()

                new_prod = []
                for x in product:
                    if x["prod_id"] and x["unit_id"] and x["retur"] and int(x["retur"]) > 0:
                        new_prod.append(
                            RsprodDdb(
                                retur.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["retur"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["totl"],
                                x["location"],
                            )
                        )

                if len(new_prod) > 0:

                    db.session.add_all(new_prod)
                    db.session.commit()

                    old_sto = StCard.query.filter(StCard.trx_code == retur.ret_code).all()
                    if old_sto:
                        for x in old_sto:
                            db.session.delete(x)
                            db.session.commit()

                    all_sto = []
                    for x in new_prod:
                        all_sto.append(
                            StCard(
                                retur.ret_code,
                                retur.ret_date,
                                "d",
                                "RTJ",
                                None,
                                x.retur,
                                x.price,
                                x.nett_price if x.nett_price and x.nett_price > 0 else x.totl,
                                None,
                                None,
                                x.disc,
                                x.prod_id,
                                x.location,
                                None,
                                0,
                                None,
                            )
                        )

                        if len(all_sto) > 0:
                            db.session.add_all(all_sto)
                            db.session.commit()

                result = response(200, "success", True, retsale_schema.dump(retur))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            retur = (
                db.session.query(RetSaleHdb, OrdpjHdb, SordHdb)
                .outerjoin(OrdpjHdb, OrdpjHdb.id == RetSaleHdb.sale_id)
                .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
                .all()
            )

            product = (
                db.session.query(RsprodDdb, ProdMdb, UnitMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == RsprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == RsprodDdb.unit_id)
                .outerjoin(LocationMdb, LocationMdb.id == RsprodDdb.location)
                .all()
            )

            result = []
            for x in retur:
                prod = []
                for y in product:
                    if x[0].id == y[0].ret_id:
                        y[0].prod_id = prod_schema.dump(y[1])
                        y[0].unit_id = unit_schema.dump(y[2])
                        y[0].location = loct_schema.dump(y[3])
                        prod.append(rsprod_schema.dump(y[0]))

                if x[1]:
                    x[1].so_id = sord_schema.dump(x[2])
                result.append(
                    {
                        "id": x[0].id,
                        "ret_code": x[0].ret_code,
                        "ret_date": RetSaleSchema(only=["ret_date"]).dump(x[0])["ret_date"]
                        if x[0].ret_date
                        else None,
                        "sale_id": ordpj_schema.dump(x[1]),
                        "product": prod,
                    }
                )

            self.response = response(200, "success", True, result)

        return self.response
