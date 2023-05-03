from ...function.update_table import UpdateTable
from ...function.update_retur_beli import UpdateReturOrd
from ...model.fkpb_hdb import FkpbHdb
from ...model.inv_pb_hdb import InvpbHdb
from ...model.stcard_mdb import StCard
from ...model.lokasi_mdb import LocationMdb
from ...model.ordpb_hdb import OrdpbHdb
from ...model.prod_mdb import ProdMdb
from ...model.supplier_mdb import SupplierMdb
from ...model.reprod_ddb import ReprodDdb
from ...model.retord_hdb import RetordHdb
from ...model.unit_mdb import UnitMdb
from ...schema.dord_hdb import DordSchema, dord_schema
from ...schema.retord_hdb import RetordSchema, retord_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.prod_mdb import prod_schema
from ...schema.reprod_ddb import reprod_schema
from ...schema.unit_mdb import unit_schema
from ...schema.lokasi_mdb import loct_schema
from ...schema.supplier_mdb import supplier_schema
from ...schema.fkpb_hdb import FkpbSchema, fkpb_schema
from ...schema.inv_pb_hdb import InvpbSchema, invpb_schema


class ReturOrder:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                ret_code = request.json["ret_code"]
                ret_date = request.json["ret_date"]
                fk_id = request.json["fk_id"]
                inv_id = request.json["inv_id"]
                product = request.json["product"]

                retur = RetordHdb(ret_code, ret_date, None, inv_id)

                db.session.add(retur)
                db.session.commit()

                new_prod = []
                for x in product:
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        and x["retur"]
                        and int(x["retur"]) > 0
                    ):
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
                                x["totl_fc"],
                            )
                        )

                if len(new_prod) > 0:

                    db.session.add_all(new_prod)
                    db.session.commit()

                UpdateReturOrd(retur.id, user.id, False)

            except IntegrityError:
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "success", True, retord_schema.dump(retur))
        else:
            try:
                retur = (
                    db.session.query(RetordHdb, InvpbHdb)
                    .outerjoin(InvpbHdb, InvpbHdb.id == RetordHdb.inv_id)
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

                    # if x[1]:
                    #     x[1].ord_id = dord_schema.dump(x[2])

                    result.append(
                        {
                            "id": x[0].id,
                            "ret_code": x[0].ret_code,
                            "ret_date": RetordSchema(only=["ret_date"]).dump(x[0])[
                                "ret_date"
                            ]
                            if x[0].ret_date
                            else None,
                            "inv_id": invpb_schema.dump(x[1]),
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "product": prod,
                        }
                    )

                return response(200, "success", True, result)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        RetordHdb,
                        FkpbHdb,
                        OrdpbHdb,
                        SupplierMdb,
                        ReprodDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        StCard,
                    ],
                    request,
                )
