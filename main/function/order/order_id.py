from main.function.update_pembelian import UpdatePembelian
from main.function.update_stock import UpdateStock
from main.model.ccost_mdb import CcostMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.inv_pb_hdb import InvpbHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.fkpb_det_ddb import FkpbDetDdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.po_mdb import PoMdb
from main.model.pprod_ddb import PprodDdb
from main.model.pjasa_ddb import PjasaDdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.unit_mdb import UnitMdb
from main.model.syarat_bayar_mdb import RulesPayMdb
from main.schema.dord_hdb import DordSchema, dord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.syarat_bayar_mdb import rpay_schema
from main.schema.dprod_ddb import dprod_schema
from main.schema.djasa_ddb import djasa_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.po_mdb import po_schema
from main.schema.ccost_mdb import ccost_schema


class OrderId:
    def __new__(self, id, request):
        do = OrdpbHdb.query.filter(OrdpbHdb.id == id).first()
        fk = (
            db.session.query(FkpbDetDdb, FkpbHdb)
            .outerjoin(FkpbHdb, FkpbHdb.id == FkpbDetDdb.fk_id)
            .filter(FkpbDetDdb.ord_id == do.id)
            .first()
        )
        if request.method == "PUT":
            try:
                ord_code = request.json["ord_code"]
                ord_date = request.json["ord_date"]
                no_doc = request.json["no_doc"]
                doc_date = request.json["doc_date"]
                faktur = request.json["faktur"]
                po_id = request.json["po_id"]
                dep_id = request.json["dep_id"]
                sup_id = request.json["sup_id"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                total_b = request.json["total_b"]
                total_bayar = request.json["total_bayar"]
                dprod = request.json["dprod"]
                djasa = request.json["djasa"]

                do.ord_code = ord_code
                do.ord_date = ord_date
                do.no_doc = no_doc
                do.doc_date = doc_date
                do.faktur = faktur
                do.po_id = po_id
                do.dep_id = dep_id
                do.sup_id = sup_id
                do.top = top
                do.due_date = due_date
                do.split_inv = split_inv
                do.prod_disc = prod_disc
                do.jasa_disc = jasa_disc
                do.total_disc = total_disc
                do.total_b = total_b
                do.total_bayar = total_bayar

                po = PoMdb.query.filter(PoMdb.id == po_id).first()
                pprod = PprodDdb.query.filter(PprodDdb.po_id == po_id).all()
                prod = DprodDdb.query.filter(DprodDdb.ord_id == id).all()
                jasa = DjasaDdb.query.filter(DjasaDdb.ord_id == id).all()

                old_prod = []
                new_prod = []
                for z in dprod:
                    if (
                        z["prod_id"]
                        and z["unit_id"]
                        and z["order"]
                        and int(z["order"]) > 0
                    ):
                        if z["id"] != 0:
                            old_prod.append(z["id"])
                        else:
                            if po_id:
                                for x in pprod:
                                    new_prod.append(
                                        DprodDdb(
                                            do.id,
                                            x["id"] if x["id"] != 0 else None,
                                            z["prod_id"],
                                            z["unit_id"],
                                            z["order"],
                                            z["price"],
                                            z["disc"],
                                            z["location"],
                                            z["nett_price"],
                                            z["total_fc"],
                                            z["total"],
                                        )
                                    )
                            else:
                                new_prod.append(
                                    DprodDdb(
                                        do.id,
                                        None,
                                        z["prod_id"],
                                        z["unit_id"],
                                        z["order"],
                                        z["price"],
                                        z["disc"],
                                        z["location"],
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
                                    for z in dprod:
                                        if z["id"] == x:
                                            if po_id:
                                                for s in pprod:
                                                    if z["pprod_id"] == s.id:
                                                        s.remain = (
                                                            y.order
                                                            - int(z["order"])
                                                            + s.remain
                                                        )
                                                        y.prod_id = z["prod_id"]
                                                        y.unit_id = z["unit_id"]
                                                        y.order = z["order"]
                                                        y.price = z["price"]
                                                        y.disc = z["disc"]
                                                        y.nett_price = z["nett_price"]
                                                        y.total_fc = z["total_fc"]
                                                        y.total = z["total"]
                                                        y.location = z["location"]

                                            else:
                                                y.prod_id = z["prod_id"]
                                                y.unit_id = z["unit_id"]
                                                y.order = z["order"]
                                                y.price = z["price"]
                                                y.disc = z["disc"]
                                                y.nett_price = z["nett_price"]
                                                y.total_fc = z["total_fc"]
                                                y.total = z["total"]
                                                y.location = z["location"]

                old_jasa = []
                new_jasa = []
                for y in djasa:
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
                                DjasaDdb(
                                    do.id,
                                    y["sup_id"],
                                    y["jasa_id"],
                                    y["unit_id"],
                                    y["order"],
                                    y["price"],
                                    y["disc"],
                                    y["total_fc"],
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
                                    for z in djasa:
                                        if z["id"] == x:
                                            y.sup_id = z["sup_id"]
                                            y.jasa_id = z["jasa_id"]
                                            y.unit_id = z["unit_id"]
                                            y.order = z["order"]
                                            y.price = z["price"]
                                            y.disc = z["disc"]
                                            y.total_fc = z["total_fc"]
                                            y.total = z["total"]

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

                if po_id:
                    remain = 0
                    for x in pprod:
                        remain += x.remain

                    if remain == 0:
                        po.status = 2
                    else:
                        po.status = 1

                    db.session.commit()

                if ns == False:
                    UpdateStock(
                        do.id, False, user_product, user_company, glUrl, request
                    )

                if faktur:
                    UpdatePembelian(
                        fk[0].id, id, False, user_product, user_company, glUrl, request
                    )

                result = response(200, "Berhasil", True, dord_schema.dump(do))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            UpdateStock(do.id, True)
            po = PoMdb.query.filter(PoMdb.id == do.po_id).first()
            if po:
                po.status = 0

                pprod = PprodDdb.query.filter(PprodDdb.po_id == do.po_id).all()
                # pjasa = PjasaDdb.query.filter(PjasaDdb.po_id == po.id).all()
                prod = DprodDdb.query.filter(DprodDdb.ord_id == do.id).all()
                # djasa = DjasaDdb.query.filter(DjasaDdb.ord_id == do.id).all()

                for y in pprod:
                    for z in prod:
                        if z.pprod_id == y.id:
                            y.remain += z.order
                        db.session.delete(z)

                db.session.commit()

            fk = (
                db.session.query(FkpbDetDdb, FkpbHdb)
                .outerjoin(FkpbHdb, FkpbHdb.id == FkpbDetDdb.fk_id)
                .filter(FkpbDetDdb.ord_id == do.id)
                .first()
            )

            inv = InvpbHdb.query.filter(InvpbHdb.ord_id == do.id).first()
            product = DprodDdb.query.filter(DprodDdb.ord_id == do.id)
            jasa = DjasaDdb.query.filter(DjasaDdb.ord_id == do.id)

            if fk:
                UpdatePembelian(fk[0].id, id, True)

            if inv:
                db.session.delete(inv)

            for x in product:
                db.session.delete(x)

            for x in jasa:
                db.session.delete(x)

            db.session.delete(do)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            x = (
                db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
                .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
                .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
                .filter(OrdpbHdb.id == id)
                .first()
            )

            dprod = (
                db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
                .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
                .all()
            )

            djasa = (
                db.session.query(DjasaDdb, JasaMdb, UnitMdb)
                .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
                .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
                .all()
            )

            product = []
            for y in dprod:
                if y[0].ord_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    y[0].lcoation = unit_schema.dump(y[3]) if y[0].location else None
                    product.append(dprod_schema.dump(y[0]))

            jasa = []
            for z in djasa:
                if z[0].ord_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(djasa_schema.dump(z[0]))

            final = {
                "id": x[0].id,
                "ord_code": x[0].ord_code,
                "ord_date": DordSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                "no_doc": x[0].no_doc,
                "doc_date": DordSchema(only=["doc_date"]).dump(x[0])["doc_date"],
                "faktur": x[0].faktur,
                "po_id": po_schema.dump(x[4]),
                "dep_id": ccost_schema.dump(x[1]),
                "sup_id": supplier_schema.dump(x[2]),
                "top": rpay_schema.dump(x[3]),
                "due_date": DordSchema(only=["due_date"]).dump(x[0])["due_date"],
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "total_b": x[0].total_b,
                "total_bayar": x[0].total_bayar,
                "status": x[0].status,
                "print": x[0].print,
                "dprod": product,
                "djasa": jasa,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
