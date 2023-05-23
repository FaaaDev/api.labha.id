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
from sqlalchemy.exc import IntegrityError
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema
from ...schema.syarat_bayar_mdb import rpay_schema
from ...schema.sprod_ddb import sprod_schema
from ...schema.sjasa_ddb import sjasa_schema
from ...schema.custom_mdb import customer_schema


class SalesOrderId:
    def __new__(self, id, request):
        so = SordHdb.query.filter(SordHdb.id == id).first()
        product = SprodDdb.query.filter(SprodDdb.so_id == id).all()
        jasa = SjasaDdb.query.filter(SjasaDdb.so_id == id).all()
        if request.method == "PUT":
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

                so.so_code = so_code
                so.so_date = so_date
                so.pel_id = pel_id
                so.ppn_type = ppn_type
                so.sub_addr = sub_addr
                so.sub_id = sub_id
                so.req_date = req_date
                so.top = top
                so.due_date = due_date
                so.split_inv = split_inv
                so.prod_disc = prod_disc
                so.jasa_disc = jasa_disc
                so.total_disc = total_disc
                so.total_bayar = total_bayar

                old_prod = []
                new_prod = []
                for x in sprod:
                    for y in product:
                        if x["id"] == y.id:
                            y.prod_id = x["prod_id"]
                            y.unit_id = x["unit_id"]
                            y.location = x["location"]
                            y.request = x["request"]
                            y.order = x["order"]
                            y.price = x["price"]
                            y.disc = x["disc"]
                            y.nett_price = x["nett_price"]
                            y.total = x["total"]
                    if x["prod_id"] and x["unit_id"] and x["order"]:
                        if x["id"] != 0:
                            old_prod.append(x["id"])
                        else:
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

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in product:
                            if y.id not in old_prod:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in sprod:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.location = z["location"]
                                            y.request = z["request"]
                                            y.order = z["order"]
                                            y.price = z["price"]
                                            y.disc = z["disc"]
                                            y.nett_price = z["nett_price"]
                                            y.total = z["total"]

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                old_jasa = []
                new_jasa = []
                for x in sjasa:
                    for y in jasa:
                        if x["id"] == y.id:
                            y.sup_id = x["sup_id"]
                            y.jasa_id = x["jasa_id"]
                            y.unit_id = x["unit_id"]
                            y.qty = x["qty"]
                            y.price = x["price"]
                            y.disc = x["disc"]
                            y.total = x["total"]
                            
                    if (x["sup_id"] and x["jasa_id"] and x["qty"]):
                        if x["id"] != 0:
                            old_jasa.append(x["id"])
                        else:
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

                if len(old_jasa) > 0:
                    for x in old_jasa:
                        for y in jasa:
                            if y.id not in old_jasa:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in sjasa:
                                        if z["id"] == x:
                                            y.sup_id = z["sup_id"]
                                            y.jasa_id = z["jasa_id"]
                                            y.unit_id = z["unit_id"]
                                            y.qty = z["qty"]
                                            y.price = z["price"]
                                            y.disc = z["disc"]
                                            y.total = z["total"]

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

                result = response(200, "Berhasil", True, sord_schema.dump(so))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            product = SprodDdb.query.filter(SprodDdb.so_id == so.id)
            jasa = SjasaDdb.query.filter(SjasaDdb.so_id == so.id)

            for x in product:
                db.session.delete(x)

            for x in jasa:
                db.session.delete(x)

            db.session.delete(so)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            x = (
                db.session.query(SordHdb, RulesPayMdb)
                .outerjoin(RulesPayMdb, RulesPayMdb.id == SordHdb.top)
                .filter(SordHdb.id == id)
                .order_by(SordHdb.id.asc())
                .first()
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

            final = {
                "id": x[0].id,
                "so_code": x[0].so_code,
                "so_date": SordSchema(only=["so_date"]).dump(x[0])["so_date"],
                "pel_id": x[0].pel_id,
                "ppn_type": x[0].ppn_type,
                "sub_addr": x[0].sub_addr,
                "sub_id": x[0].sub_id,
                "req_date": SordSchema(only=["req_date"]).dump(x[0])["req_date"],
                "top": rpay_schema.dump(x[1]),
                "due_date": SordSchema(only=["due_date"]).dump(x[0])["due_date"],
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "status": x[0].status,
                "print": x[0].print,
                "sprod": product,
                "sjasa": jasa,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
