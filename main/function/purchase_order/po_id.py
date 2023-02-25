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
from sqlalchemy.exc import IntegrityError
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


class PurchaseOrderId:
    def __new__(self, id, request):
        po = PoMdb.query.filter(PoMdb.id == id).first()
        # preq = PreqMdb.query.filter(PreqMdb.id == po.preq_id).first()
        if request.method == "PUT":
            if po.print == 0 and po.status != 2:
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
                    pprod = request.json["pprod"]
                    pjasa = request.json["pjasa"]

                    po.po_code = po_code
                    po.po_date = po_date
                    po.preq_id = preq_id
                    po.sup_id = sup_id
                    po.ref_sup = ref_sup
                    po.ppn_type = ppn_type
                    po.top = top
                    po.due_date = due_date
                    po.split_inv = split_inv
                    po.prod_disc = prod_disc
                    po.jasa_disc = jasa_disc
                    po.total_disc = total_disc
                    po.total_bayar = total_bayar

                    preq = PreqMdb.query.filter(PreqMdb.id == preq_id).first()

                    product = RprodMdb.query.filter(
                        RprodMdb.preq_id == po.preq_id
                    ).all()
                    rjasa = RjasaMdb.query.filter(RjasaMdb.preq_id == po.preq_id).all()
                    prod = PprodDdb.query.filter(PprodDdb.po_id == po.id).all()
                    jasa = PjasaDdb.query.filter(PjasaDdb.po_id == po.id).all()

                    old_prod = []
                    new_prod = []
                    for z in pprod:
                        for x in product:
                            if (
                                z["prod_id"]
                                and z["unit_id"]
                                and z["order"]
                                and int(z["order"]) > 0
                                and z["price"]
                                and int(z["price"]) > 0
                            ):
                                if z["id"] != 0:
                                    old_prod.append(z["id"])
                                else:
                                    new_prod.append(
                                        PprodDdb(
                                            po.id,
                                            preq_id,
                                            x["id"] if x["id"] != 0 else None,
                                            z["prod_id"],
                                            z["unit_id"],
                                            z["order"],
                                            z["remain"],
                                            z["price"],
                                            z["disc"],
                                            z["nett_price"],
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
                                        for z in pprod:
                                            if z["id"] == x:
                                                for s in product:
                                                    if z["rprod_id"] == s.id:
                                                        s.remain = (
                                                            y.order
                                                            - int(z["order"])
                                                            + s.remain
                                                        )
                                                        y.prod_id = z["prod_id"]
                                                        y.unit_id = z["unit_id"]
                                                        y.order = z["order"]
                                                        y.remain = z["order"]
                                                        y.price = z["price"]
                                                        y.nett_price = z["nett_price"]
                                                        y.disc = z["disc"]
                                                        y.total = z["total"]

                    old_jasa = []
                    new_jasa = []
                    for z in pjasa:
                        if (
                            z["sup_id"]
                            and z["jasa_id"]
                            and z["unit_id"]
                            and z["order"]
                            and int(x["order"]) > 0
                            and z["price"]
                            and int(z["price"]) > 0
                        ):
                            if z["id"] != 0:
                                old_jasa.append(z["id"])
                            else:
                                new_jasa.append(
                                    PjasaDdb(
                                        po.id,
                                        preq_id,
                                        None if x["id"] != 0 else None,
                                        z["sup_id"],
                                        z["jasa_id"],
                                        z["unit_id"],
                                        z["order"],
                                        z["price"],
                                        z["disc"],
                                        z["total"],
                                    )
                                )

                    if len(old_jasa) > 0:
                        for x in old_jasa:
                            for y in jasa:
                                if y.id not in old_jasa:
                                    db.session.delete(y)
                                else:
                                    if y.id == x:
                                        for z in pjasa:
                                            if z["id"] == x:
                                                for s in rjasa:
                                                    # if z["rjasa_id"] == s.id:
                                                    s.remain = (
                                                        y.order
                                                        - int(z["order"])
                                                        + s.remain
                                                    )
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

                    db.session.commit()

                    remain = 0
                    for x in product:
                        remain += x.remain
                    for x in rjasa:
                        remain += x.remain
                    if remain == 0:
                        preq.status = 2
                    else:
                        preq.status = 1

                    db.session.commit()

                    result = response(200, "Berhasil", True, po_schema.dump(po))
                except IntegrityError:
                    db.session.rollback()
                    result = response(400, "Kode sudah digunakan", False, None)
                finally:
                    self.response = result

        elif request.method == "DELETE":
            preq = PreqMdb.query.filter(PreqMdb.id == po.preq_id).first()

            if preq:
                preq.status = 0

                product = RprodMdb.query.filter(RprodMdb.preq_id == po.preq_id).all()
                jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == po.preq_id).all()
                pprod = PprodDdb.query.filter(PprodDdb.po_id == po.id).all()
                pjasa = PjasaDdb.query.filter(PjasaDdb.po_id == po.id).all()

                for y in product:
                    for z in pprod:
                        if z.rprod_id == y.id:
                            y.remain += z.order
                        db.session.delete(z)

                for y in jasa:
                    for z in pjasa:
                        if z.rjasa_id == y.id:
                            y.remain += z.order
                        db.session.delete(z)

                db.session.delete(po)
                db.session.commit()

                self.response = response(200, "Berhasil", True, None)
        else:
            x = (
                db.session.query(PoMdb, PreqMdb, CcostMdb, SupplierMdb, RulesPayMdb)
                .outerjoin(PreqMdb, PreqMdb.id == PoMdb.preq_id)
                .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
                .outerjoin(SupplierMdb, SupplierMdb.id == PoMdb.sup_id)
                .outerjoin(RulesPayMdb, RulesPayMdb.id == PoMdb.top)
                .filter(PoMdb.id == id)
                .first()
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

            final = {
                "id": x[0].id,
                "po_code": x[0].po_code,
                "po_date": PoSchema(only=["po_date"]).dump(x[0])["po_date"],
                "preq_id": {
                    "id": x[1].id,
                    "req_code": x[1].req_code,
                    "req_date": PreqSchema(only=["req_date"]).dump(x[1])["req_date"],
                    "req_dep": ccost_schema.dump(x[2]),
                    "req_ket": x[1].req_ket,
                    "status": x[1].status,
                },
                "ppn_type": x[0].ppn_type,
                "sup_id": supplier_schema.dump(x[3]),
                "ref_sup": x[0].ppn_type,
                "top": rpay_schema.dump(x[4]),
                "due_date": PoSchema(only=["due_date"]).dump(x[0])["due_date"],
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "total_bayar": x[0].total_bayar,
                "status": x[0].status,
                "apprv": x[0].apprv,
                "print": x[0].print,
                "post": x[0].post,
                "pprod": product,
                "pjasa": jasa,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
