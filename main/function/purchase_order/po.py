from main.function.update_table import UpdateTable
from main.model.pjasa_ddb import PjasaDdb
from main.model.po_mdb import PoMdb
from main.model.po_sup_ddb import PoSupDdb
from main.model.pprod_ddb import PprodDdb
from main.model.preq_mdb import PreqMdb
from main.model.rprod_mdb import RprodMdb
from main.model.rjasa_mdb import RjasaMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.ccost_mdb import CcostMdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.model.syarat_bayar_mdb import RulesPayMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.preq_mdb import PreqSchema, preq_schema
from main.schema.pprod_ddb import pprod_schema
from main.schema.pjasa_ddb import pjasa_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.syarat_bayar_mdb import rpay_schema
from main.schema.po_mdb import PoSchema, po_schema
from main.schema.po_sup_ddb import poSup_schema


class PurchaseOrder:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                po_code = request.json["po_code"]
                po_date = request.json["po_date"]
                preq_id = request.json["preq_id"]
                sup_id = request.json["sup_id"]
                ref_sup = request.json["ref_sup"]
                ppn_type = request.json["ppn_type"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                total_bayar = request.json["total_bayar"]
                ns = request.json["ns"]
                same_sup = request.json["same_sup"]
                pprod = request.json["pprod"]
                pjasa = request.json["pjasa"]
                psup = request.json["psup"]

                po = PoMdb(
                    po_code,
                    po_date,
                    preq_id,
                    sup_id,
                    ref_sup,
                    ppn_type,
                    top,
                    due_date,
                    split_inv,
                    prod_disc,
                    jasa_disc,
                    total_disc,
                    total_bayar,
                    ns,
                    same_sup,
                    0,
                    False,
                    0,
                )

                db.session.add(po)
                db.session.commit()

                preq = PreqMdb.query.filter(PreqMdb.id == preq_id).first()

                product = RprodMdb.query.filter(RprodMdb.preq_id == preq_id).all()
                jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == preq_id).all()

                new_prod = []
                for x in pprod:
                    for y in product:
                        if x["id"] == y.id:
                            y.remain = y.remain - int(x["order"])
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                        and x["price"]
                    ):
                        new_prod.append(
                            PprodDdb(
                                po.id,
                                preq_id,
                                x["id"] if x["id"] != 0 else None,
                                x["prod_id"],
                                x["unit_id"],
                                x["order"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["total"],
                            )
                        )

                new_jasa = []
                for x in pjasa:
                    for y in jasa:
                        if x["id"] == y.id:
                            y.remain = y.remain - int(x["order"])
                    if (
                        x["sup_id"]
                        and x["jasa_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                        and x["price"]
                    ):
                        new_jasa.append(
                            PjasaDdb(
                                po.id,
                                preq_id,
                                x["id"] if x["id"] != 0 else None,
                                x["sup_id"],
                                x["jasa_id"],
                                x["unit_id"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["total"],
                            )
                        )

                new_sup = []
                print(psup)
                for x in psup:
                    if (
                        x["sup_id"]
                        and x["prod_id"]
                        and x["price"]
                        and int(x["price"]) > 0
                        # and x["image"]
                    ):
                        new_sup.append(
                            PoSupDdb(
                                po.id, x["sup_id"], x["prod_id"], x["price"], x["image"]
                            )
                        )
                print(new_sup)
                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                if len(new_sup) > 0:
                    db.session.add_all(new_sup)

                db.session.commit()

                # status == 0 : belum ada po
                # status == 1 : sudah ada po, tapi produk/jasa masih sisa
                # status == 2 : selesai
                remain = 0
                for x in product:
                    remain += x.remain
                for x in jasa:
                    remain += x.remain
                if remain == 0:
                    preq.status = 2
                else:
                    preq.status = 1

                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, po_schema.dump(po))
        else:
            try:
                po = (
                    db.session.query(PoMdb, PreqMdb, CcostMdb, SupplierMdb, RulesPayMdb)
                    .outerjoin(PreqMdb, PreqMdb.id == PoMdb.preq_id)
                    .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
                    .outerjoin(SupplierMdb, SupplierMdb.id == PoMdb.sup_id)
                    .outerjoin(RulesPayMdb, RulesPayMdb.id == PoMdb.top)
                    .order_by(PoMdb.id.desc())
                    .all()
                )

                pprod = (
                    db.session.query(PprodDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == PprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == PprodDdb.unit_id)
                    .all()
                )

                pjasa = (
                    db.session.query(PjasaDdb, JasaMdb, UnitMdb)
                    .outerjoin(JasaMdb, JasaMdb.id == PjasaDdb.jasa_id)
                    .outerjoin(UnitMdb, UnitMdb.id == PjasaDdb.unit_id)
                    .all()
                )
                psup = (
                    db.session.query(PoSupDdb, SupplierMdb, ProdMdb)
                    .outerjoin(SupplierMdb, SupplierMdb.id == PoSupDdb.sup_id)
                    .outerjoin(ProdMdb, ProdMdb.id == PoSupDdb.prod_id)
                    .all()
                )

                final = []
                for x in po:
                    product = []
                    for y in pprod:
                        if y[0].po_id == x[0].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            product.append(pprod_schema.dump(y[0]))

                    jasa = []
                    for z in pjasa:
                        if z[0].po_id == x[0].id:
                            z[0].jasa_id = jasa_schema.dump(z[1])
                            z[0].unit_id = unit_schema.dump(z[2])
                            jasa.append(pjasa_schema.dump(z[0]))

                    sup = []
                    for z in psup:
                        if z[0].po_id == x[0].id:
                            z[0].sup_id = supplier_schema.dump(z[1])
                            z[0].prod_id = prod_schema.dump(z[2])
                            sup.append(poSup_schema.dump(z[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "po_code": x[0].po_code,
                            "po_date": PoSchema(only=["po_date"]).dump(x[0])["po_date"],
                            "preq_id": {
                                "id": x[1].id,
                                "req_code": x[1].req_code,
                                "req_date": PreqSchema(only=["req_date"]).dump(x[1])[
                                    "req_date"
                                ],
                                "req_dep": ccost_schema.dump(x[2]) if x[2] else None,
                                "req_ket": x[1].req_ket,
                                "status": x[1].status,
                            }
                            if x[1]
                            else None,
                            "ppn_type": x[0].ppn_type,
                            "sup_id": supplier_schema.dump(x[3]) if x[3] else None,
                            "ref_sup": x[0].ref_sup,
                            "top": rpay_schema.dump(x[4]) if x[4] else None,
                            "due_date": PoSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ]
                            if x[0].due_date
                            else None,
                            "split_inv": x[0].split_inv,
                            "prod_disc": x[0].prod_disc,
                            "jasa_disc": x[0].jasa_disc,
                            "total_disc": x[0].total_disc,
                            "total_bayar": x[0].total_bayar,
                            "ns": x[0].ns,
                            "same_sup": x[0].same_sup,
                            "status": x[0].status,
                            "apprv": x[0].apprv,
                            "print": x[0].print,
                            "pprod": product,
                            "pjasa": jasa,
                            "psup": sup,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        PoMdb,
                        PreqMdb,
                        CcostMdb,
                        SupplierMdb,
                        RulesPayMdb,
                        PprodDdb,
                        ProdMdb,
                        UnitMdb,
                        PjasaDdb,
                        JasaMdb,
                        PoSupDdb,
                    ],
                    request,
                )
