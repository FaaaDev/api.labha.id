from ...function.update_table import UpdateTable
from ...function.update_ar import UpdateAr
from ...model.custom_mdb import CustomerMdb
from ...model.jjasa_ddb import JjasaDdb
from ...model.jprod_ddb import JprodDdb
from ...model.ordpj_hdb import OrdpjHdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.sales_mdb import SalesMdb
from ...model.sord_hdb import SordHdb
from ...model.sprod_ddb import SprodDdb
from ...model.unit_mdb import UnitMdb
from ...model.syarat_bayar_mdb import RulesPayMdb
from ...model.inv_pj_hdb import InvoicePjHdb
from ...model.fkpj_hdb import FkpjHdb
from ...model.fkpj_det_ddb import FkpjDetDdb
from ...model.lokasi_mdb import LocationMdb
from ...schema.ordpj_hdb import OrdpjSchema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
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
from ...schema.lokasi_mdb import loct_schema


class Sale:
    def __new__(self, user, request):
        if request.method == "POST":
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
                total_b = request.json["total_b"]
                total_bayar = request.json["total_bayar"]
                jprod = request.json["jprod"]
                jjasa = request.json["jjasa"]

                sls = OrdpjHdb(
                    ord_code,
                    ord_date,
                    no_doc,
                    doc_date,
                    so_id,
                    invoice,
                    pel_id,
                    ppn_type,
                    sub_addr,
                    sub_id,
                    slsm_id,
                    surat_jalan,
                    req_date,
                    top,
                    due_date,
                    split_inv,
                    prod_disc,
                    jasa_disc,
                    total_disc,
                    total_b,
                    total_bayar,
                    0,
                    0,
                )

                db.session.add(sls)

                so = SordHdb.query.filter(SordHdb.id == so_id).first()
                sprod = SprodDdb.query.filter(SprodDdb.so_id == so_id).all()

                new_product = []
                for x in jprod:
                    for y in sprod:
                        if x["id"] == y.id:
                            y.remain = y.remain - int(x["order"])

                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                    ):
                        new_product.append(
                            JprodDdb(
                                sls.id,
                                x["id"] if x["id"] != 0 else None,
                                x["prod_id"],
                                x["unit_id"],
                                x["location"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["total_fc"],
                                x["total"],
                            )
                        )

                new_jasa = []
                for x in jjasa:
                    if x["jasa_id"] and x["sup_id"] and x["order"]:
                        new_jasa.append(
                            JjasaDdb(
                                sls.id,
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

                if so_id:
                    remain = 0
                    for x in sprod:
                        if x.so_id == so.id:
                            remain += x.remain

                    if remain == 0:
                        so.status = 2
                    else:
                        so.status = 1
                    print(remain)

                db.session.commit()

                UpdateAr(False, sls.id, user.id)

                invoice = InvoicePjHdb(
                    ord_code,
                    ord_date,
                    sls.id,
                    None,
                    None,
                    None,
                    total_bayar,
                    True if surat_jalan == 2 else False,
                )

                db.session.add(invoice)

                inv = InvoicePjHdb.query.filter(InvoicePjHdb.sale_id == sls.id).first()

                if surat_jalan == 2:
                    faktur = FkpjHdb(ord_code, ord_date, sls.pel_id, None, None, None)
                    db.session.add(faktur)

                    fk = FkpjHdb.query.first()
                    new_detail = FkpjDetDdb(
                        fk.id,
                        inv.id,
                        sls.id,
                        inv.inv_date,
                        sls.total_b,
                        inv.total_bayar,
                    )

                    inv.faktur = True

                    db.session.add(new_detail)

                db.session.commit()

                return response(200, "Berhasil", True, None)
            except IntegrityError:
                # print(e)
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
        else:
            try:
                sls = (
                    db.session.query(OrdpjHdb, RulesPayMdb, SordHdb, SalesMdb)
                    .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpjHdb.top)
                    .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
                    .outerjoin(SalesMdb, SalesMdb.id == OrdpjHdb.slsm_id)
                    .order_by(OrdpjHdb.id.desc())
                    .all()
                )

                cust = CustomerMdb.query.all()

                jprod = (
                    db.session.query(JprodDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == JprodDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == JprodDdb.location)
                    .all()
                )

                jjasa = (
                    db.session.query(JjasaDdb, JasaMdb, UnitMdb)
                    .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                    .outerjoin(UnitMdb, UnitMdb.id == JjasaDdb.unit_id)
                    .all()
                )

                final = []
                for x in sls:
                    product = []
                    for y in jprod:
                        if y[0].pj_id == x[0].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].location = loct_schema.dump(y[3])
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

                    final.append(
                        {
                            "id": x[0].id,
                            "ord_code": x[0].ord_code,
                            "ord_date": OrdpjSchema(only=["ord_date"]).dump(x[0])[
                                "ord_date"
                            ],
                            "no_doc": x[0].no_doc,
                            "doc_date": OrdpjSchema(only=["doc_date"]).dump(x[0])[
                                "doc_date"
                            ],
                            "so_id": sord_schema.dump(x[2]) if x[2] else None,
                            "invoice": x[0].invoice,
                            "pel_id": x[0].pel_id,
                            "ppn_type": x[0].ppn_type,
                            "sub_addr": x[0].sub_addr,
                            "sub_id": x[0].sub_id,
                            "slsm_id": sales_schema.dump(x[3]) if x[3] else None,
                            "surat_jalan": x[0].surat_jalan,
                            "req_date": OrdpjSchema(only=["req_date"]).dump(x[0])[
                                "req_date"
                            ],
                            "top": rpay_schema.dump(x[1]) if x[1] else None,
                            "due_date": OrdpjSchema(only=["due_date"]).dump(x[0])[
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
                            # "post": x[0].post,
                            # "closing": x[0].closing,
                            "jprod": product,
                            "jjasa": jasa,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        OrdpjHdb,
                        RulesPayMdb,
                        SordHdb,
                        SalesMdb,
                        JprodDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        JjasaDdb,
                        JasaMdb,
                        InvoicePjHdb,
                        FkpjHdb,
                        FkpjDetDdb,
                    ],
                    request,
                )
