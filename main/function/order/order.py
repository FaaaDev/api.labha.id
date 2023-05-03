from ...function.update_table import UpdateTable
from ...function.update_pembelian import UpdatePembelian
from ...function.update_stock import UpdateStock
from ...model.ccost_mdb import CcostMdb
from ...model.proj_mdb import ProjMdb
from ...model.djasa_ddb import DjasaDdb
from ...model.dprod_ddb import DprodDdb
from ...model.inv_pb_hdb import InvpbHdb
from ...model.fkpb_hdb import FkpbHdb
from ...model.fkpb_det_ddb import FkpbDetDdb
from ...model.lokasi_mdb import LocationMdb
from ...model.ordpb_hdb import OrdpbHdb
from ...model.pjasa_ddb import PjasaDdb
from ...model.po_mdb import PoMdb
from ...model.pprod_ddb import PprodDdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.supplier_mdb import SupplierMdb
from ...model.unit_mdb import UnitMdb
from ...model.syarat_bayar_mdb import RulesPayMdb
from ...schema.dord_hdb import DordSchema, dord_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema
from ...schema.syarat_bayar_mdb import rpay_schema
from ...schema.dprod_ddb import dprod_schema
from ...schema.djasa_ddb import djasa_schema
from ...schema.supplier_mdb import supplier_schema
from ...schema.lokasi_mdb import loct_schema
from ...schema.po_mdb import po_schema
from ...schema.ccost_mdb import ccost_schema
from ...schema.proj_mdb import proj_schema


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
                proj_id = request.json["proj_id"]
                sup_id = request.json["sup_id"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                total_b = request.json["total_b"]
                total_bayar = request.json["total_bayar"]
                ns = request.json["ns"]
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
                    proj_id,
                    sup_id,
                    top,
                    due_date,
                    split_inv,
                    prod_disc,
                    jasa_disc,
                    total_disc,
                    total_b,
                    total_bayar,
                    ns,
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

                # if do.ns == False:
                UpdateStock(do.id, False)

                if do.invoice:
                    inv = InvpbHdb(
                        ord_code,
                        ord_date,
                        do.id,
                        None,
                        None,
                        None,
                        total_bayar,
                        do.faktur,
                    )
                    print("=========fk")

                    db.session.add(inv)
                    db.session.commit()

                if do.faktur:
                    fk = FkpbHdb(ord_code, ord_date,
                                 do.sup_id, None, None, None)

                    db.session.add(fk)
                    db.session.commit()

                    invo = InvpbHdb.query.filter(
                        InvpbHdb.ord_id == do.id).first()

                    new_detail = FkpbDetDdb(
                        fk.id,
                        invo.id,
                        invo.ord_id,
                        invo.inv_date,
                        do.total_b,
                        invo.total_bayar,
                    )

                    db.session.add(new_detail)
                    db.session.commit()

                    print("=========fkkk")

                    UpdatePembelian(fk.id, user.id, False)

                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, dord_schema.dump(do))
        else:
            try:
                do = (
                    db.session.query(
                        OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb, ProjMdb
                    )
                    .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
                    .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                    .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
                    .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
                    .outerjoin(ProjMdb, ProjMdb.id == OrdpbHdb.proj_id)
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
                                loct_schema.dump(
                                    y[3]) if y[0].location else None
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
                            "proj_id": proj_schema.dump(x[5]),
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
                            "ns": x[0].ns,
                            "same_sup": x[0].same_sup,
                            "status": x[0].status,
                            "print": x[0].print,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "dprod": product,
                            "djasa": jasa,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        OrdpbHdb,
                        CcostMdb,
                        SupplierMdb,
                        RulesPayMdb,
                        PoMdb,
                        DprodDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        DjasaDdb,
                        JasaMdb,
                        InvpbHdb,
                        FkpbHdb,
                        FkpbDetDdb,
                    ],
                    request,
                )
