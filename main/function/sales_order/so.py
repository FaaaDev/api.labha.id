from ...function.update_table import UpdateTable
from ...model.custom_mdb import CustomerMdb
from ...model.sjasa_ddb import SjasaDdb
from ...model.sord_hdb import SordHdb
from ...model.sprod_ddb import SprodDdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.unit_mdb import UnitMdb
from ...model.syarat_bayar_mdb import RulesPayMdb
from ...schema.sord_hdb import SordSchema, sord_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema
from ...schema.syarat_bayar_mdb import rpay_schema
from ...schema.sprod_ddb import sprod_schema
from ...schema.sjasa_ddb import sjasa_schema
from ...schema.custom_mdb import customer_schema


class SalesOrder:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                so_code = request.json["so_code"]
                so_date = request.json["so_date"]
                pel_id = request.json["pel_id"]
                ppn_type = request.json["ppn_type"]
                sub_addr = request.json["sub_addr"]
                sub_id = request.json["sub_id"]
                req_date = request.json["req_date"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                total_bayar = request.json["total_bayar"]
                sprod = request.json["sprod"]
                sjasa = request.json["sjasa"]

                so = SordHdb(
                    so_code,
                    so_date,
                    pel_id,
                    ppn_type,
                    sub_addr,
                    sub_id,
                    req_date,
                    top,
                    due_date,
                    split_inv,
                    prod_disc,
                    jasa_disc,
                    total_disc,
                    total_bayar,
                    0,
                    0,
                )

                db.session.add(so)
                db.session.commit()

                new_prod = []
                remain = 0
                for x in sprod:
                    if x["prod_id"] and x["unit_id"] and x["order"]:
                        new_prod.append(
                            SprodDdb(
                                so.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["location"],
                                x["request"],
                                x["order"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["total"],
                            )
                        )

                new_jasa = []
                for x in sjasa:
                    if x["sup_id"] and x["jasa_id"] and x["qty"]:
                        new_jasa.append(
                            SjasaDdb(
                                so.id,
                                x["sup_id"],
                                x["jasa_id"],
                                x["unit_id"],
                                x["qty"],
                                x["price"],
                                x["disc"],
                                x["total"],
                            )
                        )

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, sord_schema.dump(so))
        else:
            try:
                so = (
                    db.session.query(SordHdb, RulesPayMdb)
                    .outerjoin(RulesPayMdb, RulesPayMdb.id == SordHdb.top)
                    .order_by(SordHdb.id.desc())
                    .all()
                )

                cust = CustomerMdb.query.all()

                sprod = (
                    db.session.query(SprodDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == SprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == SprodDdb.unit_id)
                    .all()
                )

                sjasa = (
                    db.session.query(SjasaDdb, JasaMdb, UnitMdb)
                    .outerjoin(JasaMdb, JasaMdb.id == SjasaDdb.jasa_id)
                    .outerjoin(UnitMdb, UnitMdb.id == SjasaDdb.unit_id)
                    .all()
                )

                final = []
                for x in so:
                    product = []
                    for y in sprod:
                        if y[0].so_id == x[0].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            product.append(sprod_schema.dump(y[0]))

                    jasa = []
                    for z in sjasa:
                        if z[0].so_id == x[0].id:
                            z[0].jasa_id = jasa_schema.dump(z[1])
                            z[0].unit_id = unit_schema.dump(z[2])
                            jasa.append(sjasa_schema.dump(z[0]))

                    for a in cust:
                        if a.id == x[0].pel_id:
                            x[0].pel_id = customer_schema.dump(a)

                    if x[0].sub_addr:
                        for b in cust:
                            if b.id == x[0].sub_id:
                                x[0].sub_id = customer_schema.dump(b)

                    final.append(
                        {
                            "id": x[0].id,
                            "so_code": x[0].so_code,
                            "so_date": SordSchema(only=["so_date"]).dump(x[0])[
                                "so_date"
                            ],
                            "pel_id": x[0].pel_id,
                            "ppn_type": x[0].ppn_type,
                            "sub_addr": x[0].sub_addr,
                            "sub_id": x[0].sub_id,
                            "req_date": SordSchema(only=["req_date"]).dump(x[0])[
                                "req_date"
                            ],
                            "top": rpay_schema.dump(x[1]),
                            "due_date": SordSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ],
                            "split_inv": x[0].split_inv,
                            "prod_disc": x[0].prod_disc,
                            "jasa_disc": x[0].jasa_disc,
                            "total_disc": x[0].total_disc,
                            "total_bayar": x[0].total_bayar,
                            "status": x[0].status,
                            "print": x[0].print,
                            "sprod": product,
                            "sjasa": jasa,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        SordHdb,
                        RulesPayMdb,
                        CustomerMdb,
                        SprodDdb,
                        ProdMdb,
                        UnitMdb,
                        SjasaDdb,
                        JasaMdb,
                    ],
                    request,
                )
