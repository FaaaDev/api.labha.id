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
from main.model.pjasa_ddb import PjasaDdb
from main.model.po_mdb import PoMdb
from main.model.pprod_ddb import PprodDdb
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


class Order:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                ord_code = request.json["ord_code"]
                ord_date = request.json["ord_date"]
                no_doc = request.json["no_doc"]
                doc_date = request.json["doc_date"]
                invoice = request.json["invoice"]
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
                same_sup = request.json["same_sup"]
                dprod = request.json["dprod"]
                djasa = request.json["djasa"]

                do = OrdpbHdb(
                    ord_code,
                    ord_date,
                    no_doc,
                    doc_date,
                    invoice,
                    faktur,
                    po_id,
                    dep_id,
                    sup_id,
                    top,
                    due_date,
                    split_inv,
                    prod_disc,
                    jasa_disc,
                    total_disc,
                    total_b,
                    total_bayar,
                    same_sup,
                    0,
                    0,
                )

                db.session.add(do)
                db.session.commit()

                po = PoMdb.query.filter(PoMdb.id == po_id).first()
                pprod = PprodDdb.query.filter(PprodDdb.po_id == po_id).all()
                pjasa = PjasaDdb.query.filter(PjasaDdb.po_id == po_id).all()

                new_product = []
                for x in dprod:
                    for y in pprod:
                        if x["id"] == y.id:
                            y.remain = y.remain - int(x["order"])
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                        and x["price"]
                        # and int(x["price"]) > 0
                    ):

                        new_product.append(
                            DprodDdb(
                                do.id,
                                x["id"] if x["id"] != 0 else None,
                                x["prod_id"],
                                x["unit_id"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["location"],
                                x["nett_price"],
                                x["total_fc"],
                                x["total"],
                            )
                        )

                new_jasa = []
                for x in djasa:
                    if x["jasa_id"] and x["sup_id"] and x["order"]:
                        new_jasa.append(
                            DjasaDdb(
                                do.id,
                                x["sup_id"],
                                x["jasa_id"],
                                x["unit_id"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["total_fc"],
                                x["total"],
                            )
                        )

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

                if po_id:
                    remain = 0
                    for x in pprod:
                        remain += x.remain
                    # for x in pjasa:
                    #     remain += x.remain
                    if remain == 0:
                        po.status = 2
                    else:
                        po.status = 1

                    db.session.commit()

                UpdateStock(do.id, False)

                if faktur == False and invoice == True:
                    inv = InvpbHdb(
                        ord_code, ord_date, do.id, None, None, None, total_bayar, False
                    )

                    db.session.add(inv)

                if faktur and invoice:
                    faktur = FkpbHdb(ord_code, ord_date, do.sup_id, None, None, None)
                    inv = InvpbHdb(
                        ord_code, ord_date, do.id, None, None, None, total_bayar, True
                    )

                    db.session.add(faktur)
                    db.session.add(inv)

                    invo = InvpbHdb.query.filter(InvpbHdb.ord_id == do.id).first()

                    fk = FkpbHdb.query.first()
                    new_detail = FkpbDetDdb(
                        fk.id,
                        invo.id,
                        invo.ord_id,
                        invo.inv_date,
                        do.total_b,
                        invo.total_bayar,
                    )

                    db.session.add(new_detail)

                    UpdatePembelian(
                        faktur.id,
                        user.id,
                        False,
                    )

                db.session.commit()

                result = response(200, "Berhasil", True, dord_schema.dump(do))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            do = (
                db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
                .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
                .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
                .order_by(OrdpbHdb.id.desc())
                .all()
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

            final = []
            for x in do:
                product = []
                for y in dprod:
                    if y[0].ord_id == x[0].id:
                        y[0].prod_id = prod_schema.dump(y[1])
                        y[0].unit_id = unit_schema.dump(y[2])
                        y[0].location = (
                            loct_schema.dump(y[3]) if y[0].location else None
                        )
                        product.append(dprod_schema.dump(y[0]))

                jasa = []
                for z in djasa:
                    if z[0].ord_id == x[0].id:
                        z[0].jasa_id = jasa_schema.dump(z[1])
                        z[0].unit_id = unit_schema.dump(z[2])
                        jasa.append(djasa_schema.dump(z[0]))

                final.append(
                    {
                        "id": x[0].id,
                        "ord_code": x[0].ord_code,
                        "ord_date": DordSchema(only=["ord_date"]).dump(x[0])[
                            "ord_date"
                        ],
                        "no_doc": x[0].no_doc,
                        "doc_date": DordSchema(only=["doc_date"]).dump(x[0])[
                            "doc_date"
                        ],
                        "invoice": x[0].invoice,
                        "faktur": x[0].faktur,
                        "po_id": po_schema.dump(x[4]),
                        "dep_id": ccost_schema.dump(x[1]),
                        "sup_id": supplier_schema.dump(x[2]),
                        "top": rpay_schema.dump(x[3]),
                        "due_date": DordSchema(only=["due_date"]).dump(x[0])[
                            "due_date"
                        ],
                        "split_inv": x[0].split_inv,
                        "prod_disc": x[0].prod_disc,
                        "jasa_disc": x[0].jasa_disc,
                        "total_disc": x[0].total_disc,
                        "total_b": x[0].total_b,
                        "total_bayar": x[0].total_bayar,
                        "status": x[0].status,
                        "print": x[0].print,
                        "post": x[0].post,
                        "closing": x[0].closing,
                        "dprod": product,
                        "djasa": jasa,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
