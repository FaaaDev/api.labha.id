from main.model.fkpb_hdb import FkpbHdb
from main.model.stcard_mdb import StCard
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.supplier_mdb import SupplierMdb
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
from main.schema.supplier_mdb import supplier_schema
from main.schema.fkpb_hdb import FkpbSchema, fkpb_schema


class ReturOrder:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                fk_id = request.json["fk_id"]
                product = request.json["product"]

                retur = RetordHdb(ret_code, ret_date, fk_id)


                db.session.add(retur)
                db.session.commit()

                new_prod = []
                for x in product:
                    if x["prod_id"] and x["unit_id"] and x["retur"] and int(x["retur"]) > 0:
                        new_prod.append(
                            ReprodDdb(
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
                                "k",
                                "RTB",
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

                result = response(200, "success", True, retord_schema.dump(retur))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            retur = (
                db.session.query(RetordHdb, FkpbHdb, OrdpbHdb, SupplierMdb)
                .outerjoin(FkpbHdb, FkpbHdb.id == RetordHdb.fk_id)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                .all()
            )

            product = (
                db.session.query(ReprodDdb, ProdMdb, UnitMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
                .outerjoin(LocationMdb, LocationMdb.id == ReprodDdb.location)
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
                        prod.append(reprod_schema.dump(y[0]))

                if x[1]:
                    x[1].ord_id = dord_schema.dump(x[2])
                result.append(
                    {
                        "id": x[0].id,
                        "ret_code": x[0].ret_code,
                        "ret_date": RetordSchema(only=["ret_date"]).dump(x[0])["ret_date"]
                        if x[0].ret_date
                        else None,
                        "fk_id": fkpb_schema.dump(x[1]),
                        "product": prod,
                    }
                )

            self.response = response(200, "success", True, result)

        return self.response