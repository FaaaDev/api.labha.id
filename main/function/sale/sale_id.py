from ...function.update_ar import UpdateAr
from ...model.custom_mdb import CustomerMdb
from ...model.jjasa_ddb import JjasaDdb
from ...model.jprod_ddb import JprodDdb
from ...model.inv_pj_hdb import InvoicePjHdb
from ...model.ordpj_hdb import OrdpjHdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.sales_mdb import SalesMdb
from ...model.sord_hdb import SordHdb
from ...model.sprod_ddb import SprodDdb
from ...model.unit_mdb import UnitMdb
from ...model.syarat_bayar_mdb import RulesPayMdb
from ...schema.ordpj_hdb import OrdpjSchema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema
from ...schema.syarat_bayar_mdb import rpay_schema
from ...schema.ordpj_hdb import ordpj_schema
from ...schema.custom_mdb import customer_schema
from ...schema.jprod_ddb import jprod_schema
from ...schema.jjasa_ddb import jjasa_schema
from ...schema.sales_mdb import sales_schema
from ...schema.sord_hdb import sord_schema


class SaleId:
    def __new__(self, id, request):
        sls = OrdpjHdb.query.filter(OrdpjHdb.id == id).first()
        if request.method == "PUT":
            try:
                ord_code = request.json["ord_code"]
                ord_date = request.json["ord_date"]
                no_doc = request.json["no_doc"]
                doc_date = request.json["doc_date"]
                so_id = request.json["so_id"]
                invoice = request.json["invoice"]
                pel_id = request.json["pel_id"]
                ppn_type = request.json["ppn_type"]
                sub_addr = request.json["sub_addr"]
                sub_id = request.json["sub_id"]
                slsm_id = request.json["slsm_id"]
                surat_jalan = request.json["surat_jalan"]
                req_date = request.json["req_date"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                total_bayar = request.json["total_bayar"]
                jprod = request.json["jprod"]
                jjasa = request.json["jjasa"]

                sls.ord_code = ord_code
                sls.ord_date = ord_date
                sls.no_doc = no_doc
                sls.doc_date = doc_date
                sls.so_id = so_id
                sls.invoice = invoice
                sls.pel_id = pel_id
                sls.ppn_type = ppn_type
                sls.sub_addr = sub_addr
                sls.sub_id = sub_id
                sls.slsm_id = slsm_id
                sls.surat_jalan = surat_jalan
                sls.req_date = req_date
                sls.top = top
                sls.due_date = due_date
                sls.split_inv = split_inv
                sls.prod_disc = prod_disc
                sls.jasa_disc = jasa_disc
                sls.total_disc = total_disc
                sls.total_bayar = total_bayar

                prod = JprodDdb.query.filter(JprodDdb.pj_id == sls.id)
                jasa = JjasaDdb.query.filter(JjasaDdb.pj_id == sls.id)

                so = SordHdb.query.filter(SordHdb.id == so_id).first()
                sprod = SprodDdb.query.filter(SprodDdb.so_id == so_id).all()

                old_prod = []
                new_prod = []
                for z in jprod:
                    if (
                        z["prod_id"]
                        and z["unit_id"]
                        and z["order"]
                        and int(z["order"]) > 0
                    ):

                        if z["id"] != 0:
                            old_prod.append(z["id"])
                        else:
                            for x in sprod:
                                new_prod.append(
                                    JprodDdb(
                                        sls.id,
                                        x["id"] if x["id"] != 0 else None,
                                        z["prod_id"],
                                        z["unit_id"],
                                        z["location"],
                                        z["order"],
                                        z["price"],
                                        z["disc"],
                                        z["nett_price"],
                                        z["total_fc"],
                                        z["total"],
                                    )
                                )

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in prod:
                            if y.id not in old_prod:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in jprod:
                                        if z["id"] == x:
                                            if so_id:
                                                for s in sprod:
                                                    if z["sprod_id"] == s.id:
                                                        s.remain = (
                                                            y.order
                                                            - int(z["order"])
                                                            + s.remain
                                                        )
                                                        y.prod_id = z["prod_id"]
                                                        y.unit_id = z["unit_id"]
                                                        y.order = z["order"]
                                                        y.location = z["location"]
                                                        y.price = z["price"]
                                                        y.disc = z["disc"]
                                                        y.nett_price = z["nett_price"]
                                                        y.total_fc = z["total_fc"]
                                                        y.total = z["total"]

                                            else:
                                                y.prod_id = z["prod_id"]
                                                y.unit_id = z["unit_id"]
                                                y.order = z["order"]
                                                y.location = z["location"]
                                                y.price = z["price"]
                                                y.disc = z["disc"]
                                                y.nett_price = z["nett_price"]
                                                y.total_fc = z["total_fc"]
                                                y.total = z["total"]

                old_jasa = []
                new_jasa = []
                for y in jjasa:
                    if (
                        y["sup_id"]
                        and y["jasa_id"]
                        # and x["unit_id"]
                        and y["order"]
                    ):
                        if y["id"] != 0:
                            old_jasa.append(y["id"])
                        else:
                            new_jasa.append(
                                JjasaDdb(
                                    sls.id,
                                    y["sup_id"],
                                    y["jasa_id"],
                                    y["unit_id"],
                                    y["order"],
                                    y["price"],
                                    y["disc"],
                                    y["total"],
                                )
                            )

                if len(old_jasa) > 0:
                    for x in old_jasa:
                        for y in jasa:
                            if y.id not in old_jasa:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in jjasa:
                                        if z["id"] == x:
                                            y.sup_id = z["sup_id"]
                                            y.jasa_id = z["jasa_id"]
                                            y.unit_id = z["unit_id"]
                                            y.order = z["order"]
                                            y.price = z["price"]
                                            y.disc = z["disc"]
                                            y.total = z["total"]

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                if so_id:
                    remain = 0
                    for x in sprod:
                        remain += x.remain

                    if remain == 0:
                        so.status = 2
                    else:
                        so.status = 1

                db.session.commit()

                UpdateAr(False, sls.id, id)

                result = response(200, "Berhasil", True, ordpj_schema.dump(sls))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            so = SordHdb.query.filter(SordHdb.id == sls.so_id).first()

            if so:
                so.status = 0

                sprod = SprodDdb.query.filter(SprodDdb.so_id == sls.so_id).all()
                prod = JprodDdb.query.filter(JprodDdb.pj_id == sls.id).all()

                for y in sprod:
                    for z in prod:
                        if z.sprod_id == y.id:
                            y.remain += z.order
                        db.session.delete(z)

                db.session.commit()

            UpdateAr(True, sls.id, id)

            product = JprodDdb.query.filter(JprodDdb.pj_id == sls.id)
            jasa = JjasaDdb.query.filter(JjasaDdb.pj_id == sls.id)
            inv = InvoicePjHdb.query.filter(InvoicePjHdb.sale_id == sls.id).first()

            for x in product:
                db.session.delete(x)

            for x in jasa:
                db.session.delete(x)

            if inv:
                db.session.delete(inv)

            db.session.delete(sls)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            x = (
                db.session.query(OrdpjHdb, RulesPayMdb, SordHdb, SalesMdb)
                .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpjHdb.top)
                .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
                .outerjoin(SalesMdb, SalesMdb.id == OrdpjHdb.slsm_id)
                .filter(OrdpjHdb.id == id)
                .order_by(OrdpjHdb.id.asc())
                .first()
            )

            cust = CustomerMdb.query.all()

            jprod = (
                db.session.query(JprodDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == JprodDdb.unit_id)
                .all()
            )

            jjasa = (
                db.session.query(JjasaDdb, JasaMdb, UnitMdb)
                .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                .outerjoin(UnitMdb, UnitMdb.id == JjasaDdb.unit_id)
                .all()
            )

            product = []
            for y in jprod:
                if y[0].pj_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(jprod_schema.dump(y[0]))

            jasa = []
            for z in jjasa:
                if z[0].pj_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(jjasa_schema.dump(z[0]))

            for a in cust:
                if a.id == x[0].pel_id:
                    x[0].pel_id = customer_schema.dump(a)

            if x[0].sub_addr:
                for b in cust:
                    if b.id == x[0].sub_id:
                        x[0].sub_id = customer_schema.dump(b)

            final = {
                "id": x[0].id,
                "ord_code": x[0].ord_code,
                "ord_date": OrdpjSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                "no_doc": x[0].no_doc,
                "doc_date": OrdpjSchema(only=["doc_date"]).dump(x[0])["doc_date"],
                "so_id": sord_schema.dump(x[2]) if x[2] else None,
                "invoice": x[0].invoice,
                "pel_id": x[0].pel_id,
                "ppn_type": x[0].ppn_type,
                "sub_addr": x[0].sub_addr,
                "sub_id": x[0].sub_id,
                "slsm_id": sales_schema.dump(x[3]) if x[3] else None,
                "req_date": OrdpjSchema(only=["req_date"]).dump(x[0])["req_date"],
                "top": rpay_schema.dump(x[1]) if x[1] else None,
                "due_date": OrdpjSchema(only=["due_date"]).dump(x[0])["due_date"],
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "total_bayar": x[0].total_bayar,
                "status": x[0].status,
                "print": x[0].print,
                "jprod": product,
                "jjasa": jasa,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
