
from main.function.update_table import UpdateTable
from main.function.update_rpbb import UpdateRpbb
from main.function.update_batch import updateBatch
# from main.function.write_activity import WriteActivity
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


class PenerimaanHasilJadi:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                phj_code = request.json["phj_code"]
                phj_date = request.json["phj_date"]
                batch_id = request.json["batch_id"]
                product = request.json["product"]
                reject = request.json["reject"]

                phj = PhjHdb(phj_code, phj_date, batch_id)

                db.session.add(phj)
                db.session.commit()

                new_product = []
                for x in product:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                        new_product.append(
                            PphjDdb(phj.id, x["prod_id"],
                                    x["unit_id"], x["qty"])
                        )

                new_reject = []
                for x in reject:
                    if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                        new_reject.append(
                            RphjDdb(phj.id, x["prod_id"],
                                    x["unit_id"], x["qty"])
                        )

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                if len(new_reject) > 0:
                    db.session.add_all(new_reject)

                db.session.commit()

                result = response(200, "Berhasil", True, phj_schema.dump(phj))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            try:
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
                    prod = []
                    for y in product:
                        if x[0].id == y[0].phj_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            prod.append(pphj_schema.dump(y[0]))

                    rej = []
                    for y in reject:
                        if x[0].id == y[0].phj_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            rej.append(rphj_schema.dump(y[0]))

                    if x[1]:
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

            except ProgrammingError as e:
                return UpdateTable(
                    [PhjHdb, BatchMdb, PlanHdb,
                        PphjDdb, ProdMdb, UnitMdb, RphjDdb], request
                )
