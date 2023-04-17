from ...model.preq_mdb import PreqMdb
from ...model.rprod_mdb import RprodMdb
from ...model.rjasa_mdb import RjasaMdb
from ...model.supplier_mdb import SupplierMdb
from ...model.ccost_mdb import CcostMdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.unit_mdb import UnitMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.preq_mdb import PreqSchema, preq_schema
from ...schema.rprod_mdb import rprod_schema, rprods_schema
from ...schema.rjasa_mdb import rjasa_schema, rjasas_schema
from ...schema.supplier_mdb import supplier_schema
from ...schema.ccost_mdb import ccost_schema
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema


class RequestPurchaseId:
    def __new__(self, id, request):
        preq = PreqMdb.query.filter(PreqMdb.id == id).first()
        product = RprodMdb.query.filter(RprodMdb.preq_id == id).all()
        jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == id).all()
        if request.method == "PUT":
            if preq.status == 0:
                req_code = request.json["req_code"]
                req_date = request.json["req_date"]
                req_dep = request.json["req_dep"]
                req_ket = request.json["req_ket"]
                refrence = request.json["refrence"]
                ref_sup = request.json["ref_sup"]
                ref_ket = request.json["ref_ket"]
                ns = request.json["ns"]
                rprod = request.json["rprod"]
                rjasa = request.json["rjasa"]

                preq.req_code = req_code
                preq.req_date = req_date
                preq.req_dep = req_dep
                preq.req_ket = req_ket
                preq.refrence = refrence
                preq.ref_sup = ref_sup
                preq.ref_ket = ref_ket
                preq.ns = ns

                old_prod = []
                new_prod = []

                for x in rprod:
                    if x["prod_id"] and x["unit_id"] and x["request"]:
                        if x["id"] != 0:
                            old_prod.append(x["id"])
                        else:
                            new_prod.append(
                                RprodMdb(
                                    preq.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["request"],
                                    x["request"],
                                )
                            )

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in product:
                            if y.id not in old_prod:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in rprod:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.request = z["request"]

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                old_jasa = []
                new_jasa = []

                for x in rjasa:
                    if x["jasa_id"] and x["request"]:
                        if x["id"] != 0:
                            old_jasa.append(x["id"])
                        else:
                            new_jasa.append(
                                RjasaMdb(
                                    preq.id,
                                    x["jasa_id"],
                                    x["unit_id"],
                                    x["request"],
                                    x["request"],
                                )
                            )

                if len(old_jasa) > 0:
                    for x in old_jasa:
                        for y in jasa:
                            if y.id not in old_jasa:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in rjasa:
                                        if z["id"] == x:
                                            y.jasa_id = z["jasa_id"]
                                            y.unit_id = z["unit_id"]
                                            y.request = z["request"]

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

                preq = PreqMdb.query.filter(PreqMdb.id == id).first()
                product = RprodMdb.query.filter(RprodMdb.preq_id == id).all()
                jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == id).all()
                final = {
                    "id": preq.id,
                    "req_code": preq.req_code,
                    "req_date": preq.req_date,
                    "req_dep": preq.req_dep,
                    "req_ket": preq.req_ket,
                    "refrence": preq.refrence,
                    "ref_sup": preq.ref_sup,
                    "ref_ket": preq.ref_ket,
                    "ns": preq.ns,
                    "status": preq.status,
                    "rprod": rprods_schema.dump(product),
                    "rjasa": rjasas_schema.dump(jasa),
                }

                self.response = response(200, "Berhasil", True, final)
            else:
                self.response = response(400, "Tidak dapat mengedit karena status", False, None)
        elif request.method == "DELETE":
            # if preq:
                # if preq.status == 0:
                    for x in product:
                        db.session.delete(x)
                    for x in jasa:
                        db.session.delete(x)
                    

                    db.session.delete(preq)
                    db.session.commit()
                    self.response = response(200, "Berhasil", True, None)

            # self.response = response(
            #     400, "Tidak dapat mengedit karena status tidak open", False, None
            # )
        else:
            preq = (
                db.session.query(PreqMdb, CcostMdb, SupplierMdb)
                .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
                .outerjoin(SupplierMdb, SupplierMdb.id == PreqMdb.ref_sup)
                .filter(PreqMdb.id == id)
                .first()
            )

            rprod = (
                db.session.query(RprodMdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == RprodMdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == RprodMdb.unit_id)
                .filter(RprodMdb.preq_id == id)
                .all()
            )

            rjasa = (
                db.session.query(RjasaMdb, JasaMdb, UnitMdb)
                .outerjoin(JasaMdb, JasaMdb.id == RjasaMdb.jasa_id)
                .outerjoin(UnitMdb, UnitMdb.id == RjasaMdb.unit_id)
                .filter(RjasaMdb.preq_id == id)
                .all()
            )

            prods = []
            for y in rprod:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                prods.append(rprod_schema.dump(y[0]))

            jasas = []
            for z in rjasa:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasas.append(rjasa_schema.dump(z[0]))

            final = {
                "id": preq[0].id,
                "req_code": preq[0].req_code,
                "req_date": preq[0].req_date,
                "req_dep": preq[0].req_dep,
                "req_ket": preq[0].req_ket,
                "refrence": preq[0].refrence,
                "ref_sup": preq[0].ref_sup,
                "ref_ket": preq[0].ref_ket,
                "ns": preq[0].ns,
                "status": preq[0].status,
                "rprod": prods,
                "rjasa": jasas,
            }

            self.response = response(200, "Berhasil", True, final)

        return self.response
