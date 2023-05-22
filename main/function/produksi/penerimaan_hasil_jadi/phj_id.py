from main.model.batch_mdb import BatchMdb
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.plan_hdb import PlanHdb
from main.model.phj_hdb import PhjHdb
from main.model.pphj_ddb import PphjDdb
from main.model.rphj_ddb import RphjDdb
from main.model.fprod_ddb import FprodDdb
from main.model.msn_mdb import MsnMdb
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.batch_mdb import batch_schema, BatchSchema
from main.schema.plan_hdb import plan_schema, PlanSchema
from main.schema.phj_hdb import phj_schema, PhjSchema
from main.schema.pphj_ddb import pphj_schema
from main.schema.rphj_ddb import rphj_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.msn_mdb import msn_schema
from main.schema.plmch_ddb import plmch_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.lokasi_mdb import loct_schema


class PenerimaanHasilJadiId:
    def __new__(self, id, request):
        x = PhjHdb.query.filter(PhjHdb.id == id).first()
        if request.method == "PUT":
            try:
                phj_code = request.json["phj_code"]
                phj_date = request.json["phj_date"]
                batch_id = request.json["batch_id"]
                product = request.json["product"]
                reject = request.json["reject"]

                x.phj_code = phj_code
                x.phj_date = phj_date
                x.batch_id = batch_id

                db.session.commit()

                old_product = PphjDdb.query.filter(PphjDdb.phj_id == id).all()
                new_product = []
                for z in product:
                    if z["id"]:
                        for y in old_product:
                            if z["id"] == y.id:
                                if (
                                    z["id"]
                                    and z["prod_id"]
                                    and z["unit_id"]
                                    and z["qty"]
                                    and int(z["qty"]) > 0
                                ):
                                    y.prod_id = z["prod_id"]
                                    y.unit_id = z["unit_id"]
                                    y.qty = z["qty"]
                    else:
                        if z["prod_id"] and z["unit_id"] and z["qty"] and int(z["qty"]) > 0:
                            new_product.append(
                                PphjDdb(
                                    x.id,
                                    z["prod_id"],
                                    z["unit_id"],
                                    z["qty"],
                                )
                            )

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                old_reject = RphjDdb.query.filter(RphjDdb.phj_id == id).all()
                new_reject = []
                for z in reject:
                    if z["id"]:
                        for y in old_reject:

                            if z["id"] == y.id:
                                if (
                                    z["id"]
                                    and z["prod_id"]
                                    and z["unit_id"]
                                    and z["qty"]
                                    and int(z["qty"]) > 0
                                ):
                                    y.prod_id = z["prod_id"]
                                    y.unit_id = z["unit_id"]
                                    y.qty = z["qty"]
                    else:
                        if z["prod_id"] and z["unit_id"] and z["qty"] and int(z["qty"]) > 0:
                            new_reject.append(
                                RphjDdb(
                                    x.id,
                                    z["prod_id"],
                                    z["unit_id"],
                                    z["qty"],
                                )
                            )

                if len(new_reject) > 0:
                    db.session.add_all(new_reject)

                db.session.commit()

                result = response(200, "Berhasil", True, phj_schema.dump(x))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        elif request.method == "DELETE":
            old_product = PphjDdb.query.filter(PphjDdb.phj_id == id).all()
            old_reject = RphjDdb.query.filter(RphjDdb.phj_id == id).all()

            if old_product:
                for y in old_product:
                    db.session.delete(y)

            if old_reject:
                for y in old_reject:
                    db.session.delete(y)

            db.session.delete(x)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            phj = (
                db.session.query(PhjHdb, BatchMdb, PlanHdb)
                .outerjoin(BatchMdb, BatchMdb.id == PhjHdb.batch_id)
                .outerjoin(PlanHdb, PlanHdb.id == BatchMdb.plan_id)
                .order_by(PhjHdb.id.desc())
                .all()
            )

            product = (
                db.session.query(PphjDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == PphjDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == PphjDdb.unit_id)
                .all()
            )

            reject = (
                db.session.query(RphjDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == RphjDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == RphjDdb.unit_id)
                .all()
            )

            final = []
            for x in phj:
                if x[0].id == id:
                    prod = []
                    for y in product:
                        if x[1].id == y[0].phj_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            prod.append(pphj_schema.dump(y[0]))

                    rej = []
                    for y in reject:
                        if x[1].id == y[0].phj_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            rej.append(rphj_schema.dump(y[0]))

                    x[1].plan_id = plan_schema.dump(x[2])
                    final.append(
                        {
                            "id": x[0].id,
                            "phj_code": x[0].phj_code,
                            "phj_date": PhjSchema(only=["phj_date"]).dump(x[0])["phj_date"],
                            "batch_id": batch_schema.dump(x[1]),
                            "product": prod,
                            "reject": rej,
                        }
                    )

            return response(200, "Berhasil", True, final)

        return self.response
